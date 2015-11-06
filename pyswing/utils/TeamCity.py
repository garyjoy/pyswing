class TeamCity(object):
    """
    The (Static) TeamCity class provides an interface to the TeamCity Build Script Interaction.

    https://confluence.jetbrains.com/display/TCD8/Build+Script+Interaction+with+TeamCity
    """

    @staticmethod
    def setBuildResultText(buildResultText, appendExisting = True):
        """
        Sets the Build Result Text in TeamCity.

        :param buildResultText: Text to use for the Build Result Text in TeamCity.
        :param appendExisting: Boolean Flag indicating that the existing Build Result Text should be appended. Default value is True.
        """

        if appendExisting:
            print("##teamcity[buildStatus text='" + buildResultText + " ({build.status.text})']")
        else:
            print("##teamcity[buildStatus text='" + buildResultText + "']")
