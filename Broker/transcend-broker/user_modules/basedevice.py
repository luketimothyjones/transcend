# basedevice.py
# ---
# Part of the Transcend library
# Specifies the base class for user-implemented devices
# ---
# Luke Jones, 2017
# --------

# See BasicRGBLight.py for an example implementation.


class Device:

    def __init__(self, address, object_name):
        """
        This is the superclass (base class) for all Transcend Devices. Do not modify the
        code here; instead, create a new Python file in this directory and subclass it.
        Then, use the descriptions in each method's docstring to write code that will work
        with your device.

        Refer to your game developer's documentation for details regarding
        the data format sent from, and expected by, the associated in-game object.

        Once you have met the design requirements listed here you are done! Put your device
        information into the configuration file and Transcend will take care of the rest.

        :param address: The network address of the device. If you are using the requests
                        library, make sure you include a protocol. Also, make sure you
                        provide a port if it does not match the protocol!

        :param object_name: Name of the object in-game
        """

        self.address = address
        self.object_name = object_name

    # ---------
    def format_for_device(self, data):
        """
        Takes information about the in-game object and translates it into a format that
        the device can understand. This data will be passed to self.send()

        :param data: Data received from the in-game object, in JSON format
        :return: Data formatted to match the device's format requirements
        """

        raise NotImplementedError

    # ---
    def send(self, data):
        """

        :param data:
        :return:
        """

        raise NotImplementedError

    # ---------
    def format_for_game(self, data):
        """
        Translates data received from the device into a format that the game
        object can understand. Use this in self.update() to clean data up before
        we return it to the game.

        :param data: Data received from the device via self.receive()
        :return: Data formatted to match the in-game object's data format (in JSON)
        """

        raise NotImplementedError

    # ---
    def update(self):
        """
        Gets information from the device, such as whether it is on or off.
        This method is called by Transcend every time the game requests an update,
        so optimization is good!

        :return: Two values: status code, data (where data has been formatted
                 to fit the in-game object's data format)
        """

        raise NotImplementedError
