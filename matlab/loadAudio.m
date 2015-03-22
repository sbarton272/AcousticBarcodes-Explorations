function [audioFiles, Fs] = loadAudio()

FILE_START = '../audio/black011001-';
ENCODING = [1 1 0 1 1 0 0 1 1 1]; % start/stop bands of [1 1]
FILE_END = '.wav';
FILE_NUMS = 1:9;

audioFiles = cell(1,length(FILE_NUMS));

i = 1;
for fileNum = FILE_NUMS
    fileName = [FILE_START, num2str(fileNum), FILE_END];
    [y2, Fs] = audioread(fileName);
    audioFiles{i}.audio = y2;
    audioFiles{i}.name = fileName;
    audioFiles{i}.encoding = ENCODING;
    i = i + 1;
end

end