import io
import select
import subprocess as sp
import sys
import os
import shutil
from typing import Dict, Tuple, Optional, IO

sys.path.append("demucs")
os.environ["PATH"] += os.pathsep + os.path.abspath("demucs")

class DemucsProcessor:
    def __init__(self, num_threads=4, segment_size=10):
        self.num_threads = num_threads
        self.segment_size = segment_size

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
                    std.write(buf)
                    output += buf

            return output

        model = "htdemucs" if num_stems != "6" else "htdemucs_6s"
        demucs_path = os.path.join(os.path.abspath("demucs"), "demucs")

        cmd = [
            "python",
            "-m",
            "demucs.separate",
            "-n", model,
            "-o", "tracks",
            f"{filename}.{filetype}",
            "-d", "cpu",
            "-j", str(self.num_threads),
            "--segment", str(self.segment_size),
            "--overlap", "0.1"  # Reduce overlap for speed
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
        print("With command: ", " ".join(cmd))
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        output = copy_process_streams(p)
        p.wait()
        if p.returncode != 0:
            print("Command failed, something went wrong.")

        filename_without_ext = os.path.splitext(filename)[0]
        output_dir = f"tracks/{model}/{filename_without_ext}"
        os.makedirs(output_dir, exist_ok=True)
        shutil.make_archive(f"STEMS-{filename_without_ext}", "zip", output_dir)

        return output
