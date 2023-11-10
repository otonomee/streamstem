import io
from pathlib import Path
import select
from shutil import rmtree
import subprocess as sp
import sys
import shutil
from typing import Dict, Tuple, Optional, IO
import requests

class DemucsProcessor:
    def process_audio(self, filename):

        # Customize the following options!
        model = "htdemucs"
        extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.
        two_stems = None   # only separate one stems from the rest, for instance
        # two_stems = "vocals"

        # Options for the output audio.
        mp3 = True
        mp3_rate = 320
        float32 = False  # output as float 32 wavs, unsused if 'mp3' is True.
        int24 = False    # output as int24 wavs, unused if 'mp3' is True.
        # You cannot set both `float32 = True` and `int24 = True` !!

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
                    raw_buf = p_stream.read(2 ** 16)
                    if not raw_buf:
                        fds.remove(fd)
                        continue
                    buf = raw_buf.decode()
                    std.write(buf)  # write to server terminal
                    output += buf   # store in string

            return output

        
        
        cmd = ["python3", "-m", "demucs.separate", "-n", model, "-o", "tracks", filename]
        if mp3:
            cmd += ["--mp3", f"--mp3-bitrate={mp3_rate}"]
        if float32:
            cmd += ["--float32"]
        if int24:
            cmd += ["--int24"]
        if two_stems is not None:
            cmd += [f"--two-stems={two_stems}"]
        
        print("Going to separate the file:", filename)
        print(cmd)
        print("With command: ", " ".join(cmd))
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        output = copy_process_streams(p)
        p.wait()
        if p.returncode != 0:
            print("Command failed, something went wrong.")

        shutil.make_archive(f"{filename}_separated", 'zip', f"tracks/{filename}")
        
        return output
