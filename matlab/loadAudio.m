function [audioFiles, Fs] = loadAudio()

FILE_START = '../audio/black011001-*';
ENCODING = [1 1 0 1 1 0 0 1 1 1]; % start/stop bands of [1 1]
% FILE_START = '../audio/1110101-*';
% ENCODING = [1 1 1 0 1 0 1];
FILE_END = '.wav';

% audioFiles = cell(1,length(FILE_NUMS));

audioFiles = dir(FILE_START);

% i = 1;
for i = 1:length(audioFiles)
%     fileName = [FILE_START, num2str(fileNum), FILE_END];
    fileName = audioFiles(i).name;
    [y2, Fs] = audioread(['../audio/' fileName]);
    audioFiles(i).audio = y2;
%     audioFiles{i}.name = fileName;
    audioFiles(i).encoding = ENCODING;
%     i = i + 1;
end

end
