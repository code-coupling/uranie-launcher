""" Module used to set uncertainty data into an understandable format for uranie_launcher.
"""
from pathlib import Path
from typing import List


class Inputs():
    """ Class containing all the info about all the uncertain parameters.
    """
    class Distribution():  # pylint: disable=too-few-public-methods
        """ Class containing the info about the distribution for a specific uncertain parameter.
        """
        def __init__(self):
            pass

        # TODO string conversion
        # def __str__(self) -> str:
        #     return ''

    class DistributionUniform(Distribution):
        """Define the lower and upper bounds of a uniform distribution.

        Parameters
        ----------
        lower_bound : float
            lower bound of the distribution
        upper_bound : float
            upper bound of the distribution
        """
        def __init__(self, lower_bound, upper_bound):
            super().__init__()
            if lower_bound < upper_bound:
                self._lower_bound = lower_bound
                self._upper_bound = upper_bound
            else:
                raise ValueError("The upper bound have to be greater than the lower one !")

        @property
        def lower_bound(self) -> float:
            """Returns info about the distribution

            Returns
            -------
            float
                lower bound of the distribution
            """
            return self._lower_bound

        @property
        def upper_bound(self) -> float:
            """Returns info about the distribution

            Returns
            -------
            float
                upper bound of the distribution
            """
            return self._upper_bound

    class DistributionTruncatedNormal(Distribution):
        """ Set the arguments needed to define a truncated normal distribution.

        Parameters
        ----------
        lower_bound : float
            lower bound of the distribution
        upper_bound : float
            upper bound of the distribution
        mean : float
            mean of the distribution
        standard_deviation : float
            standard deviation of the distribution
        """
        def __init__(self, lower_bound, upper_bound, mean, standard_deviation):
            super().__init__()
            if lower_bound < upper_bound:
                self._lower_bound = lower_bound
                self._upper_bound = upper_bound
                self._mean = mean
                self._standard_deviation = standard_deviation
            else:
                raise ValueError("The upper bound have to be greater than the lower one !")

        @property
        def lower_bound(self) -> float:
            """Returns all info about the distribution

            Returns
            -------
            float
                lower bound of the distribution
            """
            return self._lower_bound

        @property
        def upper_bound(self) -> float:
            """Returns all info about the distribution

            Returns
            -------
            float
                upper bound of the distribution
            """
            return self._upper_bound

        @property
        def mean(self) -> float:
            """Returns all info about the distribution

            Returns
            -------
            float
                mean
            """
            return self._mean

        @property
        def standard_deviation(self) -> float:
            """Returns all info about the distribution

            Returns
            -------
            float
                standard deviation
            """
            return self._standard_deviation

    class Input():
        """ Class containing all the info about one specific parameter of the uncertain parameters.
        """
        def __init__(self, variable_name: str, distribution: 'Inputs.Distribution'):
            """ Set all the info about one specific parameter of the uncertain parameters.

            Parameters
            ----------
            variable_name : str
                Name of the uncertain variable
            distribution : Inputs.Distribution
                Is the distribution_info object previously defined
            """
            self._variable_name = variable_name
            self._distribution = distribution
            self._flag_delimiter = '@'

        @property
        def variable_name(self) -> str:
            """Returns the name of the uncertain value

            Returns
            -------
            str
                variable name
            """
            return self._variable_name

        @property
        def distribution(self) -> 'Inputs.Distribution':
            """Returns all info about the distribution

            Returns
            -------
            'Inputs.Distribution'
                distribution
            """
            return self._distribution

        @property
        def flag(self) -> str:
            """Returns the flag

            Returns
            -------
            str
                flag
            """
            return f"{self._flag_delimiter}{self._variable_name}{self._flag_delimiter}"

    def __init__(self):
        self._inputs = []
        self._file_flag = ""

    def add_input(self, _input: Input):
        """Adds an input class object into an inputs class list which contains all information
        about all uncertain parameters.

        Parameters
        ----------
        _input : Input
            Object containing all the info about one specific parameter of the uncertain parameters.
        """
        self._inputs.append(_input)

    @property
    def inputs(self) -> List[Input]:
        """Returns the _inputs list that contains all info about each uncertain parameter

        Returns
        -------
        list
            inputs
        """
        return self._inputs

    def set_file_flag(self, file_flag: Path):
        """ Set the name of the file containing the balise_flag which will be replaced
        by a specific value depending on the chosen distribution.

        Parameters
        ----------
        file_flag : Path
            Should be something like : <file_name>_Balise.<ext>
        """
        self._file_flag = file_flag

    @property
    def file_flag(self) -> str:
        """Returns the name of the file containing the balise

        Returns
        -------
        str
            file flag
        """
        return self._file_flag


class Propagation():
    """ Class defining an object containing the name
    of the propagation method used and the sample size.
    """

    SOBOL = "Sobol"
    """Sobol is blablabla... TODO"""

    SRS = "SRS"
    """SRS is blablabla... TODO"""

    def __init__(self, sampling_method: str, sample_size: int):
        if sample_size <= 0:
            raise ValueError("sample_size must be greater than 0")

        self._sampling_method = sampling_method
        self._sample_size = sample_size

    @property
    def sampling_method(self) -> str:
        """Returns the sampling method

        Returns
        -------
        str
            sampling method name
        """
        return self._sampling_method

    @property
    def sample_size(self) -> int:
        """Get the sample size variable

        Returns
        -------
        int
            sample size
        """
        return self._sample_size


class Outputs():
    """ Class defining an object containing all the informations about the outputs.
    """

    class Output():
        """ Class containing all the info about one specific output.
        """
        def __init__(self, headers: List[str], quantity_of_interest: str, filename: str):
            """Constructor.

            Parameters
            ----------
            headers : List[str]
                Names of the aggregation functions applied on the output
            quantity_of_interest : str
                Names of the output
            filename : str
                Name of the output file, if any
            """
            self._headers = headers
            self._quantity_of_interest = quantity_of_interest
            self._filename = filename

        @property
        def headers(self) -> List[str]:
            """Returns the dictionary containing all the chosen aggregation functions

            Returns
            -------
            list
                headers
            """
            return self._headers

        @property
        def quantity_of_interest(self) -> str:
            """Returns the name of the quantity of interest

            Returns
            -------
            str
                quantity_of_interest
            """
            return self._quantity_of_interest

        @property
        def filename(self) -> str:
            """Returns the name of the output file, if any

            Returns
            -------
            str
                file name
            """
            return self._filename

    def __init__(self, name):
        self._outputs = []
        self._name = name

    def add_output(self, output: 'Outputs.Output'):
        """ Set all the info about one specific output.

        Parameters
        ----------
        output : Outputs.Output
            output
        """
        self._outputs.append(output)

    @property
    def outputs(self) -> List[Output]:
        """Returns a list of the outputs containing all the info about each output

        Returns
        -------
        List[Output]
            outputs
        """
        return self._outputs

    @property
    def name(self) -> str:
        """Returns the name of the output

        Returns
        -------
        str
            tds_name
        """
        return self._name

    @property
    def experimental_design_filename(self) -> str:
        """Returns the name of the experimental design file

        Returns
        -------
        str
            ``self.name+'_exp_design.dat')``
        """
        return f"{self.name}_exp_design.dat"

    @property
    def output_filename(self) -> str:
        """Returns the name of the output file

        Returns
        -------
        str
            ``self.name+'_output.dat')``
        """
        return f"{self.name}_output.dat"

    @property
    def failed_filename(self) -> str:
        """Returns the name of the failed file

        Returns
        -------
        str
            ``self.name+'_failed.dat')``
        """
        return f"{self.name}_failed.dat"
