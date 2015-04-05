function [decoded, errs] = runAcousticBarcodes(audioFileObj, Fs)

disp(['Decoding ', audioFileObj.name]);
audio = sum(audioFileObj.audio, 2);

%% Pre-Filter noise
fltY = preFilter(audio, false);

%% Transients
trans = transients(fltY,Fs, false);

%% Plot found locations
% plotTransientLocs(trans, audio, Fs);

%% Decode
decoded = decodeBarcode(trans, false);

%% Errors
errs = countErrs(decoded, audioFileObj.encoding);

end
