#
# SOMA - Copyright (C) CEA, 2015
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
#

# System import
import logging
import os

# Define the logger
logger = logging.getLogger(__name__)

# Soma import
from soma.qt_gui.qt_backend import QtGui, QtCore
from soma.controller import trait_ids
from soma.qt_gui.timered_widgets import TimeredQLineEdit
from soma.functiontools import partial

# Qt import
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class ScrollControllerWidget(QtGui.QScrollArea):

    """ Class that create a widget to set the controller parameters.

    The widget is placed in a scroll area when large sets of parameters have
    to be tuned.
    """

    def __init__(self, controller, parent=None, name=None, live=False,
                 hide_labels=False, select_controls=None,
                 disable_controller_widget=False):
        """ Method to initilaize the ScrollControllerWidget class.

        Parameters
        ----------
        controller: derived Controller instance (mandatory)
            a class derived from the Controller class we want to parametrize
            with a widget.
        parent: QtGui.QWidget (optional, default None)
            the controller widget parent widget.
        name: (optional, default None)
            the name of this controller widget
        live: bool (optional, default False)
            if True, synchronize the edited values in the widget with the
            controller values on the fly,
            otherwise, wait synchronization instructions to update the
            controller values.
        hide_labels: bool (optional, default False)
            if True, don't show the labels associated with the controls
        select_controls: str (optional, default None)
            parameter to select specific conrtoller traits. Authorized options
            are 'inputs' or 'outputs'.
        disable_controller_widget: bool (optional, default False)
            if True disable the controller widget.
        """
        # Inheritance
        super(ScrollControllerWidget, self).__init__(parent)

        # Allow the application to resize the scroll area items
        self.setWidgetResizable(True)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
                           QtGui.QSizePolicy.Preferred)

        # Display a surounding box
        self.setFrameShape(QtGui.QFrame.StyledPanel)

        # Create the controller widget
        self.controller_widget = ControllerWidget(
            controller, parent, name, live, hide_labels, select_controls)
        self.controller_widget.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                             QtGui.QSizePolicy.Preferred)

        # Enable / disabled the controller widget
        self.controller_widget.setEnabled(not disable_controller_widget)

        # Set the controller widget in the scroll area
        self.setWidget(self.controller_widget)

    def __del__(self):
        # disconnect underlying ControllerWidget so that it can be deleted.
        self.controller_widget.disconnect()


class DeletableLineEdit(QtGui.QWidget):

    """ Close button + line editor, used for modifiable key labels
    """
    userModification = QtCore.Signal()
    buttonPressed = QtCore.Signal()

    def __init__(self, text=None, parent=None):
        super(DeletableLineEdit, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)
        delete_button = QtGui.QToolButton()
        layout.addWidget(delete_button)
        # Set the tool icons
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            _fromUtf8(":/soma_widgets_icons/delete")),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        delete_button.setIcon(icon)
        self.line_edit = TimeredQLineEdit(text)
        layout.addWidget(self.line_edit)
        self.line_edit.userModification.connect(self.userModification)
        delete_button.pressed.connect(self.buttonPressed)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)


class ControllerWidget(QtGui.QWidget):

    """ Class that create a widget to set the controller parameters.
    """

    # Parameter to store the mapping between the string trait descriptions and
    # the associated control classes
    _defined_controls = {}

    def __init__(self, controller, parent=None, name=None, live=False,
                 hide_labels=False, select_controls=None,
                 editable_labels=False):
        """ Method to initilaize the ControllerWidget class.

        Parameters
        ----------
        controller: derived Controller instance (mandatory)
            a class derived from the Controller class we want to parametrize
            with a widget.
        parent: QtGui.QWidget (optional, default None)
            the controller widget parent widget.
        name: (optional, default None)
            the name of this controller widget
        live: bool (optional, default False)
            if True, synchronize the edited values in the widget with the
            controller values on the fly,
            otherwise, wait the synchronization instruction to update the
            controller values.
        hide_labels: bool (optional, default False)
            if True, don't show the labels associated with the controls
        select_controls: str (optional, default None)
            parameter to select specific conrtoller traits. Authorized options
            are 'inputs' or 'outputs'.
        editable_labels: bool (optional, default False)
            if True, labels (trait keys) may be edited by the user, their
            modification will trigger a signal.
        """
        # Inheritance
        super(ControllerWidget, self).__init__(parent)

        QtCore.QResource.registerResource(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'resources', 'widgets_icons.rcc'))

        # Class parameters
        self.controller = controller
        self.live = live
        self.hide_labels = hide_labels
        self.select_controls = select_controls
        # Parameter to store the connection status between the
        # controller widget and the controller
        self.connected = False
        # Parameter to store all the controller widget controls:
        # the keys correspond to the control name (a control name is
        # associated to a controller trait with the same name), the
        # dictionary elements are 4-uplets of the form (trait, control_class,
        # control_instance, control_label).
        self._controls = {}
        self._keys_connections = {}
        self.editable_labels = editable_labels

        # If possilbe, set the widget name
        if name:
            self.setObjectName(name)

        # Create the layout of the controller widget
        # We will add all the controls to this layout
        self._grid_layout = QtGui.QGridLayout()
        self._grid_layout.setAlignment(QtCore.Qt.AlignTop)
        self._grid_layout.setSpacing(3)
        self._grid_layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self._grid_layout)

        # Create all the layout controls associated with the controller values
        # we want to tune (ie the user traits)
        self._create_controls()
        self.connect_keys()

        # Start the event loop that check for wrong edited fields (usefull
        # when we work off line, otherwise the traits make the job but it is
        # still user friendly).
        self._check()

        # Set the synchrinization between this object and the input controller:
        # 1) synchronize the edited values in the widget with the controller
        # values on the fly
        if self.live:
            self.connect()

        # 2) initialize the controller widget with the controller values and
        # wait synchronization instructions to update the controller values.
        else:
            self.update_controller_widget()

    #
    # Public members
    #

    def is_valid(self):
        """ Check that all edited fields are correct.

        Returns
        -------
        valid: bool
            True if all the controller widget controls are correctly filled,
            False otherwise
        """
        # Initilaized the output
        valid = True

        # Go through all the controller widget controls
        for control_name, control in self._controls.iteritems():

            # Unpack the control item
            trait, control_class, control_instance, control_label = control

            # Call the current control specific check method
            valid = control_class.is_valid(control_instance)

            # Stop checking if a wrong control has been found
            if not valid:
                break

        return valid

    def update_controller(self):
        """ Update the controller.

        At the end the controller traits values will match the controller
        widget user defined parameters.
        """
        # Go through all the controller widget controls
        for control_name, control in self._controls.iteritems():

            # Unpack the control item
            trait, control_class, control_instance, control_label = control

            # Call the current control specific update controller method
            control_class.update_controller(self, control_name,
                                            control_instance)

    def update_controller_widget(self):
        """ Update the controller widget.

        At the end the controller widget user editable parameters will match
        the controller traits values.
        """
        # Go through all the controller widget controls
        for control_name, control in self._controls.iteritems():

            # Unpack the control item
            trait, control_class, control_instance, control_label = control

            # Call the current control specific update controller widget method
            control_class.update_controller_widget(self, control_name,
                                                   control_instance)

    def connect(self):
        """ Connect the controller trait and the controller widget controls

        At the end al control will be connected with the associated trait, and
        when a 'user_traits_changed' signal is emited, the controls are updated
        (ie, deleted if necessary).
        """
        # If the controller and controller widget are not yet connected
        if not self.connected:

            # Go through all the controller widget controls
            for control_name, control in self._controls.iteritems():

                # Unpack the control item
                trait, control_class, control_instance, control_label = control

                # Call the current control specific connection method
                logger.debug("Connecting control '{0}: {1}'...".format(
                    control_name, control_instance))
                control_class.connect(self, control_name, control_instance)

            # Add an event connected with the 'user_traits_changed' controller
            # signal: update the controls
            self.controller.on_trait_change(self.update_controls,
                                            "user_traits_changed")

            # Update the controller widget values
            self.update_controller_widget()

            # Update the connection status
            self.connected = True

    def connect_keys(self):
        if not self.editable_labels or self._keys_connections:
            return
        keys_connect = {}
        # Go through all the controller widget controls
        for control_name, control in self._controls.iteritems():
            hook1 = partial(self._key_modified, control_name)
            hook2 = partial(self._delete_key, control_name)
            control = self._controls[control_name]
            label_control = control[3]
            if isinstance(label_control, tuple):
                label_control = label_control[0]
            label_control.userModification.connect(hook1)
            label_control.buttonPressed.connect(hook2)
            keys_connect[control_name] = (label_control, hook1, hook2)
        self._keys_connections = keys_connect

    def disconnect(self):
        """ Disconnect the controller trait and the controller widget controls
        """
        # If the controller and controller widget are connected
        if self.connected:

            # Remove the 'update_controls' event connected with the
            # 'user_traits_changed' controller signal
            self.controller.on_trait_change(
                self.update_controls, "user_traits_changed", remove=True)

            # Go through all the controller widget controls
            for control_name, control in self._controls.iteritems():

                # Unpack the control item
                trait, control_class, control_instance, control_label = control

                # Call the current control specific disconnection method
                control_class.disconnect(self, control_name, control_instance)

            # Update the connection status
            self.connected = False

    def disconnect_keys(self):
        for control_name, connections in self._keys_connections.iteritems():
            label_widget, hook1, hook2 = connections
            label_widget.userModification.disconnect(hook1)
            label_widget.buttonPressed.disconnect(hook2)
        self._keys_connections = {}

    def update_controls(self):
        """ Event to refresh controller widget controls and intern parameters.

        The refresh is done off line, ie. we need first to disconnect the
        controller and the controller widget.
        """
        # Get the controller traits
        user_traits = self.controller.user_traits()

        # Assess the refreshing is done off line
        was_connected = self.connected
        if was_connected:
            self.disconnect()
        self.disconnect_keys()

        # Go through all the controller widget controls
        to_remove_controls = []
        for control_name, control in self._controls.iteritems():

            # Message
            logger.debug(
                "Check if we need to update '{0}': trait in '{1}' "
                "different from '{2}'?".format(
                    control_name, control, user_traits.get(control_name)))

            # Unpack the control item
            trait, control_class, control_instance, control_label = control

            # If the the controller trait is different from the trait
            # associated with the control
            if user_traits.get(control_name) != trait:

                # Close and schedule for deletation the control widget
                control_instance.close()
                control_instance.deleteLater()

                # Close and schedule for deletation the control labels
                if isinstance(control_label, tuple):
                    for label in control_label:
                        label.close()
                        label.deleteLater()
                elif control_label:
                    control_label.close()
                    control_label.deleteLater()

                # Store the controls to be removed
                to_remove_controls.append(control_name)

        # Delete all dead controls from the class '_controls' intern parameter
        for control_name in to_remove_controls:
            logger.debug("Delete control '{0}'.".format(control_name))
            del self._controls[control_name]

        # Recreate all the layout controls associated with the controller
        # values we want to tune (ie the user_traits): this procedure check
        # if the control has not already been created.
        self._create_controls()

        # Restore the connection status
        if was_connected:
            self.connect()
        self.connect_keys()

        # Update the widget geometry
        self.updateGeometry()

    #
    # Private members
    #

    def _check(self):
        """ Check that all edited fields are correct.

        At the end the controls with wrong values will be colored in red.
        """
        # Go through all the controller widget controls
        for control_name, control in self._controls.iteritems():

            # Unpack the control item
            trait, control_class, control_instance, control_label = control

            # Call the current control specific check method
            control_class.check(control_instance)

    def _create_controls(self):
        """ Method that will create a control for each user trait of the
        controller.

        Controller trait parameters that cannot be maped to controls
        will not appear in the user interface.
        """
        # Select only the controller traits of interest
        all_traits = self.controller.user_traits()
        if self.select_controls is None:
            slected_traits = all_traits
        elif self.select_controls == "inputs":
            slected_traits = dict(
                (trait_name, trait)
                for trait_name, trait in all_traits.iteritems()
                if trait.output == False)
        elif self.select_controls == "outputs":
            slected_traits = dict(
                (trait_name, trait)
                for trait_name, trait in all_traits.iteritems()
                if trait.output == True)
        else:
            raise Exception(
                "Unrecognized 'select_controls' option '{0}'. Valid "
                "options are 'inputs' or 'outputs'.".format(self.select_controls))

        # Go through all the controller user traits
        for trait_name, trait in slected_traits.iteritems():

            # Create the widget
            self.create_control(trait_name, trait)

    def create_control(self, trait_name, trait):
        """ Create a control associated to a trait.

        Parameters
        ----------
        trait_name: str (mandatory)
            the name of the trait from which we want to create a control. The
            control widget will share the same name
        trait: Trait (mandatory)
            a trait item
        """
        # Search if the current trait has already been processed
        control = self._controls.get(trait_name)

        # If no control has been found in the class intern parameters
        if control is None:

            # Call the search function that will map the trait type to the
            # corresponding control type
            control_class = self.get_control_class(trait)

            # If no control has been found, skip this trait and print
            # an error message. Note that the parameter will not be
            # accessible in the user interface.
            if control_class is None:
                logger.error(
                    "No control defined for trait '{0}': {1}. This "
                    "parameter will not be accessible in the "
                    "user interface.".format(trait_name, trait_ids(trait)))
                return

            # Create the control instance and associated label
            if self.editable_labels:
                label_class = DeletableLineEdit
            else:
                label_class = QtGui.QLabel
            control_instance, control_label = control_class.create_widget(
                self, trait_name, getattr(self.controller, trait_name),
                trait, label_class)
            control_class.is_valid(control_instance)

            # If the trait contains a description, insert a tool tip to the
            # control instance
            tooltip = ""
            if trait.desc:
                tooltip = "<b>" + trait_name + ":</b> " + trait.desc
            control_instance.setToolTip(tooltip)

            # Get the last empty row in the grid layout
            # Trick: If the grid layout is empty check the element 0
            # (not realistic but te grid layout return None)
            last_row = self._grid_layout.rowCount()
            widget_item = self._grid_layout.itemAtPosition(last_row, 1)
            while widget_item is None and last_row > 0:
                last_row -= 1
                widget_item = self._grid_layout.itemAtPosition(last_row, 1)
            last_row += 1

            # If the control has no label, append the control in a two
            # columns span area of the grid layout
            if control_label is None:

                # Grid layout 'addWidget' parameters: QWidget, int row,
                # int column, int rowSpan, int columnSpan
                self._grid_layout.addWidget(
                    control_instance, last_row, 0, 1, 2)

            # If the control has two labels, add a first row with the
            # labels (one per column), and add the control in
            # the next row of the grid layout in the second column
            elif isinstance(control_label, tuple):

                # Get the number of label
                nb_of_labels = len(control_label)

                # If more than two labels are detected, print an error message.
                # We actually consider only the two first labels and skip the
                # others
                if nb_of_labels > 2:
                    logger.error("To many labels associated with control "
                                 "'{0}': {1}. Only consider the two first "
                                 "labels and skip the others".format(
                                     trait_name, control_label))

                # Append each label in different columns
                if not self.hide_labels:
                    self._grid_layout.addWidget(
                        control_label[0], last_row, 0)
                if nb_of_labels >= 2:
                    self._grid_layout.addWidget(control_label[1], last_row, 1)

                # Append the control in the next row in the second column
                self._grid_layout.addWidget(control_instance, last_row + 1, 1)

            # Otherwise, append the label and control in two separate
            # columns of the grid layout
            else:

                # Append the label in the first column
                if not self.hide_labels:
                    self._grid_layout.addWidget(control_label, last_row, 0)

                # Append the control in the second column
                self._grid_layout.addWidget(
                    control_instance, last_row, 1, 1, 1)

            # Store some informations about the inserted control in the
            # private '_controls' class parameter
            # Keys: the trait names
            # Parameters: the trait - the control name - the control - and
            # the labels associated with the control
            self._controls[trait_name] = (
                trait, control_class, control_instance, control_label)

        # Otherwise, the control associated with the current trait name is
        # already inserted in the grid layout, just unpack the values
        # contained in the private '_controls' class parameter
        else:
            trait, control_class, control_instance, control_label = control

        # Convert 'control_label' parameter to tuple
        control_label = control_label or ()
        if not isinstance(control_label, tuple):
            control_label = (control_label, )

        # Each trait has a hidden property. Take care of this information
        hide = getattr(trait, "hidden", False)

        # Hide the control and associated labels
        if hide:
            control_instance.hide()
            for label in control_label:
                label.hide()

        # Show the control and associated labels
        else:
            control_instance.show()
            for label in control_label:
                label.show()

    def _key_modified(self, old_key):
        """ Dict / open controller key modification callback
        """
        control_label = self._controls[old_key][3]
        if isinstance(control_label, tuple):
            control_label = control_label[0]
        key = str(control_label.text())
        was_connected = self.connected
        if was_connected:
            self.disconnect()
        self.disconnect_keys()

        controller = self.controller
        trait = controller.trait(old_key)
        controller.add_trait(key, trait)
        setattr(controller, key, getattr(controller, old_key))
        controller.remove_trait(old_key)
        self._controls[key] = self._controls[old_key]
        del self._controls[old_key]
        if was_connected:
            self.connect()
        # reconnect label widget
        self.connect_keys()
        # self.update_controls()  # not even needed
        if hasattr(self, 'main_controller_def'):
            main_control_class, controller_widget, control_name, frame = \
                self.main_controller_def
            main_control_class.update_controller(
                controller_widget, control_name, frame)
        # self.update_controller()

    def _delete_key(self, key):
        """ Dict / open controller key deletion callback
        """
        controller = self.controller
        trait = controller.trait(key)
        controller.remove_trait(key)
        self.update_controls()
        if hasattr(self, 'main_controller_def'):
            main_control_class, controller_widget, control_name, frame = \
                self.main_controller_def
            main_control_class.update_controller(
                controller_widget, control_name, frame)
        # self.update_controller()

    #
    # Class Methods
    #
    @classmethod
    def get_control_class(cls, trait):
        """ Find the control associated with the input trait.

        The mapping is defined in the global class parameter
        '_defined_controls'.

        Parameters
        ----------
        cls: ControllerWidget (mandatory)
            a ControllerWidget class
        trait: Trait (mandatory)
            a trait item

        Returns
        -------
        control_class: class
            the control class associated with the input trait.
            If no match has been found, return None
        """
        # Initilaize the output variable
        control_class = None

        # Go through the trait string description: can have multiple element
        # when either trait is used
        # Todo:: we actualy need to create all the controls and let the user
        # choose which one he wants to fill.
        for trait_id in trait_ids(trait):

            # Recursive construction: consider only the top level
            trait_id = trait_id.split("_")[0]

            # Try to get the control class
            control_class = cls._defined_controls.get(trait_id)

            # Stop when we have a match
            if control_class is not None:
                break

        return control_class


from soma.qt_gui.controls import controls

# Fill the controller widget mapping between the string trait descriptions and
# the associated control classes
ControllerWidget._defined_controls.update(controls)
