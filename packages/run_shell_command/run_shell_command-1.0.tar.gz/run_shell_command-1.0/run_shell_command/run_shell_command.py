import logging
import pipes
import subprocess
import shlex


def run_shell_command(command, format_args=None, format_kwargs=None, returncode=False):
    """Run a shell string as if it was run from bash. This supports piping"""

    if format_args is not None:
        # Escape arguments for format.
        format_args = [pipes.quote(str(arg)) for arg in format_args]
        # pylint: disable=star-args
        command = command.format(*format_args)

    if format_kwargs is not None:
        # Escape arguments for format.
        format_kwargs_keys = format_kwargs.keys()
        format_kwargs_values = [pipes.quote(str(arg)) for arg in format_kwargs.values()]
        format_kwargs = dict(itertools.izip(format_kwargs_keys, format_kwargs_values))

    logging.debug(command)

    commands = [cmd.strip() for cmd in command.split('|')]

    prevous_process = None
    process_list = []

    for command in commands:

        # Use shlex so that quoted strings won't get split
        process_as_list = shlex.split(command)

        if prevous_process is None:
            process = subprocess.Popen(
                process_as_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            process = subprocess.Popen(
                process_as_list,
                stdin=prevous_process.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # The .stdout.close() call is important in order to receive a
            # SIGPIPE in the previous processes.
            # https://docs.python.org/2/library/subprocess.html#replacing-shell-pipeline
            prevous_process.stdout.close()

        # Remember the processes.
        process_list.append(process)
        prevous_process = process

    out, err = process.communicate()

    # Collect the exit codes of the subprocesses.
    for proc in process_list:
        proc.wait()

    if returncode:
        return (out, err, process.returncode)

    return (out, err)
