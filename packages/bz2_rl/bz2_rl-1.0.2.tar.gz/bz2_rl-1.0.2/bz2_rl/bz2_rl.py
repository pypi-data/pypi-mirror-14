# (C) 2016, MIT license

'''
BZ2TextFileStreamer main code.
'''
from bz2 import BZ2Decompressor

bz2de = BZ2Decompressor()


class BZ2TextFileStreamer:
    '''
    Iterates through a bzip2 compressed text file, decoding as it goes along
    and yielding lines one by one until the end of the file. Since the file
    is not completely contained in memory, it can be used to decode
    and process very large text files line-by-line efficiently.
    '''

    def __init__(self, bz2_file=None, encoding='utf-8', read_size=512,
                 linebreak=b'\n'):
        '''
        Sets up the streamer.

        :param bz2_file: path to the bzip2 compressed file, or None
        :param encoding: Text encoding
        :param read_size: Number of bytes to read at a time
        :param linebreak: Linebreak to look for (\n by default)
        '''
        self.file = None
        self.encoding = encoding
        self.read_size = read_size
        self.linebreak = linebreak

        if bz2_file is not None:
            self.file = open(bz2_file, 'rb')

    def set_file(self, file):
        '''
        Sets the file stream manually, in case you prefer to open the file
        yourself.
        '''
        self.file = file

    def _close(self):
        '''
        Closes the file.
        '''
        if self.file is not None:
            self.file.close()

    def __del__(self):
        '''
        Ensures that the file is closed on destruction.
        '''
        self._close()

    def __iter__(self):
        '''
        Iterator that runs through the compressed file and yields only
        full lines explicitly terminated by a linebreak.
        '''
        # String buffer that will contain decompressed text.
        buffer = b''

        while True:
            # Read a series of compressed bytes.
            file_bytes = self.file.read(self.read_size)

            if file_bytes == b'':
                # File has reached EOF, so close it and stop iteration
                # after yielding the remaining line of the file.
                yield buffer.decode(self.encoding)
                self._close()
                return

            # Decompress bytes and interpret using the correct encoding.
            buffer += bz2de.decompress(file_bytes)

            # Yield lines if we have any; put the remainder back in the buffer.
            if self.linebreak in buffer:
                lines = buffer.split(self.linebreak)

                for line in lines[:-1]:
                    yield (line + self.linebreak).decode(self.encoding)

                buffer = lines[-1]
