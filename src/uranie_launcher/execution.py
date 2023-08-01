"""Class used to set execution info into an understandable format for uranie_launcher.
"""
from pathlib import Path


class Execution:
    """ Parent class of classes describing how to execute the calculations.
    """
    def __init__(self, working_directory: Path) -> None:
        """Constructor.

        Parameters
        ----------
        working_directory : Path
            Path to the working directory of Uranie Launcher.
        """
        self._working_directory = working_directory
        self._visualization = False
        self._clean = True
        self._save = -1

    @property
    def working_directory(self) -> Path:
        """Path to the working directory of Uranie Launcher.

        Returns
        -------
        Path
            Path to the directory
        """
        return self._working_directory

    @property
    def visualization(self) -> bool:
        """Get the visialisation status

        Returns
        -------
        bool
            Enabled if True
        """
        return self._visualization

    @property
    def clean(self) -> bool:
        """Get the cleanning status

        Returns
        -------
        bool
            Enabled if True
        """
        return self._clean

    @property
    def save(self) -> int:
        """Get the saving status

        Returns
        -------
        bool
            Enabled if True
        """
        return self._save

    def enable_visualization(self, enable: bool = True):
        """To enable/disable visualization

        Parameters
        ----------
        enable : bool, optional
            True to enable, by default True
        """
        self._visualization = enable

    def clean_outputs(self, enable: bool = True):
        """To enable/disable cleanning

        From Uranie documentation: set the clean flag to the value true or false. If it is set to
        True, all the working directories are cleaned before launching. Then if the save flag is
        set to True, the working directories are cleaned a second time after the TLauncher run.
        If not specified, default parameter is kTrue, which means the working directory will be
        cleaned (i.e. temporary folders will be erased)

        Parameters
        ----------
        enable : bool, optional
            True to enable, by default True
        """
        self._clean = enable

    def save_outputs(self, enable: int = -1):
        """To enable/disable saving

        From Uranie documentation: activate the save mode and set the maximum number i of
        folders to be kept. A positive value for i stands for the explicit maximum number of saves,
        while no value or -1 value allow to keep all the patterns (all patterns are launched in a
        different working directory UranieLauncher_i). Default parameter is -1.
        If setSave is not called, the temporary output folders of the code will be overwritten at
        each computing step, while they will be left unmodified if the method is called.

        Example
        -------
        >>> mylauncher.setSave() # will save each launch
        >>> mylauncher.setSave(-1) # will save each launch
        >>> mylauncher.setSave(10) # will save 10 launches

        Warning
        -------
        In case of multi-process distributed computation, in order to prevent all the processes
        from trying and accessing the same data at the same time, a call to the setSave method is
        mandatory. As a consequence, if it is not manually set, Uranie will set it automatically

        Parameters
        ----------
        enable : int, optional
            True to enable, by default -1
        """
        self._save = enable


class ExecutionLocal(Execution):
    """Object containing the info about how to execute the calculations on a desktop.
    """
    def __init__(self, working_directory: Path, nb_jobs: int = 1) -> None:
        """Constructor.

        Parameters
        ----------
        working_directory : Path
            Path to the working directory of Uranie Launcher.
        nb_jobs : int, optional
            Number of parallel executions, by default 1.

        Raises
        ------
        ValueError
            'nb_jobs' must be >=1.
        """
        super().__init__(working_directory=working_directory)
        if nb_jobs < 1:
            raise ValueError(f"'nb_jobs' ({nb_jobs}) must be >=1.")
        self._nb_jobs = nb_jobs

    @property
    def nb_jobs(self):
        """Get the number of jobs

        Returns
        -------
        int
            value >0
        """
        return self._nb_jobs


class ExecutionSlurm(Execution):
    """Object containing the info about how to execute the calculations on a cluster using SLURM.
    """
    def __init__(self):
        super().__init__(working_directory="")
        # TODO implementer l'execution sur cluster
        raise NotImplementedError("Execution on cluster is not implemented yet")
#         self._nb_of_tasks = 1
#         self._nb_of_cpu_per_task = 10
#         self._memory_per_cpu = "100M"
#         self._partitions = "amdq_naples,amdq_rome,intelq_5118,intelq_6226,intelq_6234"
#         self._qos = "normal"
#         self._account = ""
#         self._walltime = "01:00:00"
#         self._job_name = "my_job"
#         self._output_file = "output_file.out"
#         self._error_file = "error_file"
#         self._email = "your.name@example.com"
#         self._email_type = "ALL"
#         self._liste_of_nodes = ""
#         self._myscript_to_launch = "myscript.sh"

#     def set_nb_of_tasks(self, nb_of_tasks: int):
#         """Set the number of tasks

#         Parameters
#         ----------
#         execution_mode : int
#             Set _nb_of_tasks
#         """
#         self._nb_of_tasks = nb_of_tasks

#     @property
#     def nb_of_tasks(self):
#         """Get the number of tasks

#         Returns
#         -------
#         int
#             self._nb_of_tasks
#         """
#         return self._nb_of_tasks


#     def set_nb_of_cpu_per_task(self, nb_of_cpu_per_task: int):
#         """Set the number of CPU per tasks

#         Parameters
#         ----------
#         execution_mode : int
#             Set _nb_of_cpu_per_task
#         """
#         self._nb_of_cpu_per_task = nb_of_cpu_per_task

#     @property
#     def nb_of_cpu_per_task(self):
#         """Get the number of CPU per tasks

#         Returns
#         -------
#         int
#             self._nb_of_cpu_per_task
#         """
#         return self._nb_of_cpu_per_task


#     def set_memory_per_cpu(self, memory_per_cpu: str):
#         """Set the memory per cpu

#         Parameters
#         ----------
#         execution_mode : str
#             Set _memory_per_cpu
#         """
#         self._memory_per_cpu = memory_per_cpu

#     @property
#     def memory_per_cpu(self):
#         """Get the memory per cpu

#         Returns
#         -------
#         str
#             self._memory_per_cpu
#         """
#         return self._memory_per_cpu


#     def set_partitions(self, partitions: str):
#         """Set the partitions

#         Parameters
#         ----------
#         execution_mode : str
#             Set _partitions
#         """
#         self._partitions = partitions

#     @property
#     def partitions(self):
#         """Get the partitions

#         Returns
#         -------
#         str
#             self._partitions
#         """
#         return self._partitions


#     def set_qos(self, qos: str):
#         """Set the QoS (Quality of Service)

#         Parameters
#         ----------
#         execution_mode : str
#             Set _qos
#         """
#         self._qos = qos

#     @property
#     def qos(self):
#         """Get the QoS (Quality of Service)

#         Returns
#         -------
#         str
#             self._qos
#         """
#         return self._qos


#     def set_account(self, account: str):
#         """Set the account

#         Parameters
#         ----------
#         execution_mode : str
#             Set _account
#         """
#         self._account = account

#     @property
#     def account(self):
#         """Get the account

#         Returns
#         -------
#         str
#             self._account
#         """
#         return self._account

#     def set_walltime(self, walltime: str):
#         """Set the walltime (format : HH:MM:SS)

#         Parameters
#         ----------
#         execution_mode : str
#             Set _walltime
#         """
#         self._walltime = walltime

#     @property
#     def walltime(self):
#         """Get the walltime

#         Returns
#         -------
#         str
#             self._walltime
#         """
#         return self._walltime


#     def set_job_name(self, job_name: str):
#         """Set the job name

#         Parameters
#         ----------
#         execution_mode : str
#             Set _job_name
#         """
#         self._job_name = job_name

#     @property
#     def job_name(self):
#         """Get the job name

#         Returns
#         -------
#         str
#             self._job_name
#         """
#         return self._job_name


#     def set_output_file(self, output_file: str):
#         """Set the output file name

#         Parameters
#         ----------
#         execution_mode : str
#             Set _output_file
#         """
#         self._output_file = output_file

#     @property
#     def output_file(self):
#         """Get the output file name

#         Returns
#         -------
#         str
#             self._output_file
#         """
#         return self._output_file


#     def set_error_file(self, error_file: str):
#         """Set the error file name

#         Parameters
#         ----------
#         execution_mode : str
#             Set _error_file
#         """
#         self._error_file = error_file

#     @property
#     def error_file(self):
#         """Get the error file name

#         Returns
#         -------
#         str
#             self._error_file
#         """
#         return self._error_file


#     def set_email(self, email: str):
#         """Set the email by which you will be notified

#         Parameters
#         ----------
#         execution_mode : str
#             Set _email
#         """
#         self._email = email

#     @property
#     def email(self):
#         """Get the email by which you will be notified

#         Returns
#         -------
#         str
#             self._email
#         """
#         return self._email


#     def set_email_type(self, email_type: str):
#         """Set the type of event for which you want to be notified by email

#         Parameters
#         ----------
#         execution_mode : str
#             Set _email_type
#         """
#         self._email_type = email_type

#     @property
#     def email_type(self):
#         """Get the type of event for which you want to be notified by email

#         Returns
#         -------
#         str
#             self._email_type
#         """
#         return self._email_type


#     def set_liste_of_nodes(self, liste_of_nodes: str):
#         """_summary_

#         Parameters
#         ----------
#         execution_mode : str
#             Set _liste_of_nodes
#         """
#         self._liste_of_nodes = liste_of_nodes

#     @property
#     def liste_of_nodes(self):
#         """_summary_

#         Returns
#         -------
#         str
#             self._liste_of_nodes
#         """
#         return self._liste_of_nodes


#     def set_myscript_to_launch(self, myscript_to_launch: str):
#         """Set the name of the script to launch

#         Parameters
#         ----------
#         execution_mode : str
#             Set _myscript_to_launch
#         """
#         self._myscript_to_launch = myscript_to_launch

#     @property
#     def myscript_to_launch(self):
#         """Get the name of the script to launch

#         Returns
#         -------
#         str
#             self._myscript_to_launch
#         """
#         return self._myscript_to_launch
