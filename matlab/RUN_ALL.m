%% Run basic algorithm on all 1101100111 files

clear all
close all

%% Load
[audioFiles, Fs] = loadAudio();
N = length(audioFiles);
errs = zeros(1,N);
for i = 1:N
    disp(['Decoding ', audioFiles{i}.name]);
    audio = sum(audioFiles{i}.audio, 2);

    %% Pre-Filter noise
    fltY = preFilter(audio, false);

    %% Transients
    trans = transients(fltY,Fs);

    %% Plot found locations
    plotTransientLocs(trans, audio, Fs);

    %% Decode
    decoded = decodeBarcode(trans, true, Fs);

    %% Errors
    code = audioFiles{i}.encoding;
    m = length(code);
    n = length(decoded);
    if m > n
        decoded = [decoded, -ones(1,m-n)];
    else
        code = [code, -ones(1,n-m)];
    end
    if i == 8 % these audio samples are backwards!
        code = flip(code);
    end

    errs(i) = sum(decoded ~= code);

end

figure; stem(errs); title('Errors');
