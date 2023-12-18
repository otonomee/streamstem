import io
import select
import subprocess as sp
import sys
sys.path.append('demucs')
import shutil
from typing import Dict, Tuple, Optional, IO
import os
os.environ["PATH"] += os.pathsep + os.path.abspath("demucs")
import os


class DemucsProcessor:
    def process_audio(self, filename, filetype, num_stems):
        def copy_process_streams(process: sp.Popen):
            output = ""

            def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
                assert stream is not None
                if isinstance(stream, io.BufferedIOBase):
                    stream = stream.raw
                return stream

            p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
            stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
                p_stdout.fileno(): (p_stdout, sys.stdout),
                p_stderr.fileno(): (p_stderr, sys.stderr),
            }
            fds = list(stream_by_fd.keys())

            while fds:
                ready, _, _ = select.select(fds, [], [])
                for fd in ready:
                    p_stream, std = stream_by_fd[fd]
                    raw_buf = p_stream.read(2**16)
                    if not raw_buf:
                        fds.remove(fd)
                        continue
                    buf = raw_buf.decode()
                    std.write(buf)  # write to server terminal
                    output += buf  # store in string

            return output

        model = "htdemucs"
        if num_stems == "6":
            model = "htdemucs_6s"

        demucs_path = os.path.join(os.path.abspath("demucs"), "demucs")

        cmd = [
                "python3",
                "-m",
                "demucs.separate",
                "-n",
                model,
                "-o",
                "tracks",
                f"{filename}.{filetype}",
            ]

        if filetype == "mp3":
            cmd += ["--mp3", "--mp3-bitrate=320"]
        elif filetype == "flac":
            cmd += ["--flac"]
        else:
            print("Filetype error")

        if num_stems == "2":
            cmd += ["--two-stems", "vocals"]

        print("Going to separate the file:", f"{filename}.{filetype}")
        print(cmd)
        print("With command: ", " ".join(cmd))
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        output = copy_process_streams(p)
        p.wait()
        if p.returncode != 0:
            print("Command failed, something went wrong.")

        filename_without_ext = os.path.splitext(filename)[0]

        output_dir = f"tracks/htdemucs/{filename_without_ext}"
        if model == "htdemucs_6s":
            output_dir = f"tracks/htdemucs_6s/{filename_without_ext}"

        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        shutil.make_archive(f"STEMS-{filename_without_ext}", "zip", output_dir)

        # # Delete the directory
        # shutil.rmtree('tracks/htdemucs', ignore_errors=True)
        # shutil.rmtree('tracks/htdemucs_6s', ignore_errors=True)

        # # Recreate the directories
        # os.makedirs('tracks/htdemucs', exist_ok=True)
        # os.makedirs('tracks/htdemucs_6s', exist_ok=True)

        return output
