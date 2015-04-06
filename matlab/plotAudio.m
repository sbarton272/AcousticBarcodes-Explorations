function plotAudio(y, Fs)

SPEC_WIN = 32;

if size(y,2) == 2
    % Make single channel
    y = sum(y,2);
end

%% Viz

w = linspace(-1,1,length(y));
t = linspace(0,length(y)/Fs,length(y));

figure;
title('Single Channel');
subplot(3,1,1); plot(w,fftshift(abs(fft(y))));
subplot(3,1,2); plot(t,y);
subplot(3,1,3);
spectrogram(y,SPEC_WIN,'yaxis');

end
