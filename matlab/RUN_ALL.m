%% Run basic algorithm on all 1101100111 files

clear all
close all

%% Load
[audioFiles, Fs] = loadAudio();
N = length(audioFiles);
errs = zeros(1,N);
for i = 1:N
    [decoded, e] = runAcousticBarcodes(audioFiles{i}, Fs);
    errs(i) = e;
end

figure; stem(errs); title('Errors');
