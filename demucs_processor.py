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
    def __init__(self, num_threads, segment_size):
        self.num_threads = num_threads
        self.segment_size = segment_size

    def process_audio(self, filename: str, filetype: str, num_stems: int) -> str:
        """
        Process audio file with Demucs to separate stems.

        Args:
            filename: Name of audio file (without extension)
            filetype: File extension (mp3, wav, flac)
            num_stems: Number of stems to separate (2, 4, or 6)

        Returns:
            str: Command output

        Raises:
            RuntimeError: If Demucs processing fails
            ValueError: If parameters are invalid
        """
        # Convert num_stems to int if it's a string (from API)
        if isinstance(num_stems, str):
            try:
                num_stems = int(num_stems)
            except ValueError:
                raise ValueError(f"Invalid num_stems value: {num_stems}. Must be 2, 4, or 6.")

        # Validate num_stems
        if num_stems not in [2, 4, 6]:
            raise ValueError(f"Invalid num_stems: {num_stems}. Must be 2, 4, or 6.")

        # Validate filetype
        valid_filetypes = ["mp3", "wav", "flac"]
        if filetype not in valid_filetypes:
            raise ValueError(f"Invalid filetype: {filetype}. Must be one of {valid_filetypes}")

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

        model = "htdemucs" if num_stems != 6 else "htdemucs_6s"
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

        if num_stems == 2:
            cmd += ["--two-stems", "vocals"]

        print("Going to separate the file:", f"{filename}.{filetype}")
        print("With command: ", " ".join(cmd))
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        output = copy_process_streams(p)
        p.wait()

        # Check for process failure
        if p.returncode != 0:
            error_msg = f"Demucs separation failed with return code {p.returncode}. Output: {output}"
            print(error_msg)
            raise RuntimeError(error_msg)

        filename_without_ext = os.path.splitext(filename)[0]
        output_dir = f"tracks/{model}/{filename_without_ext}"

        # Validate output directory exists and contains files
        if not os.path.exists(output_dir):
            error_msg = f"Output directory not created: {output_dir}"
            print(error_msg)
            raise RuntimeError(error_msg)

        output_files = os.listdir(output_dir)
        if not output_files:
            error_msg = f"No stem files generated in {output_dir}"
            print(error_msg)
            raise RuntimeError(error_msg)

        print(f"Successfully generated {len(output_files)} stem files: {output_files}")

        # Create zip archive of separated stems
        os.makedirs(output_dir, exist_ok=True)
        shutil.make_archive(f"STEMS-{filename_without_ext}", "zip", output_dir)

        return output
