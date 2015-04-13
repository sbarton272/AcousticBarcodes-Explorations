function fltY = preFilter(y, verbose)

SPEC_WIN = 32;
S = abs(spectrogram(y,SPEC_WIN));

%% Normalize bands
m = mean(S,2);
s = std(S,0,2);

normS = bsxfun(@times, bsxfun(@minus, S, m), 1 ./ s);

% Weight the freq bins
weights = ones(size(normS,1),1);
weights(1:20) = 0;
wNormS = bsxfun(@times, normS, weights);
sumS = sum(wNormS);

fltY = sumS;

if verbose
    figure; imagesc(normS); title('Normed S');
    figure; imagesc(wNormS); title('Weighted normed S');
    figure; plot(sumS); title('Sum over S');
end

end