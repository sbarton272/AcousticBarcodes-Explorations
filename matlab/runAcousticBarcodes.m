function [decoded, errs] = runAcousticBarcodes(audioFileObj)

disp(['Decoding ', audioFileObj.name]);
audio = sum(audioFileObj.audio, 2);

%% Pre-Filter noise
fltY = preFilter(audio, false);

%% Transients
trans = transients(fltY,Fs);

%% Plot found locations
plotTransientLocs(trans, audio, Fs);

%% Decode
decoded = decodeBarcode(trans, true);

%% Errors
errs = countErrs(decoded, audioFileObj.encoding);

end