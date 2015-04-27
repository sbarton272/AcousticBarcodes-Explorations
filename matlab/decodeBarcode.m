function decoded = decodeBarcode(trans, bPlot, Fs)

ONE_ENCODE = 1;
ZERO_ENCODE = 2;

% make sure there is something to decode
if length(trans) < 4 % 4 guard bits
    decoded = [];
    return
end

iois = diff(trans);
iois = flip(iois);

% For plotting purposes
unitLengthAvg = zeros(1,length(iois));

%TODO add in unit length detection
%TODO discrimination by thresholding ioi ratios
%TODO unit length interpolation curve

% Decide if interonset delay is encoding 0 or 1 based on which multiple of
% unitLen it is closer to

% Find the first two guard bits, 11, and get the unit length from that
for g = 1:length(iois) - 2
    if isWithinThresold(iois(g), iois(g+1))
        unitLength = iois(g)*.2 + iois(g+1)*.8;
        unitLengthAvg(g) = iois(g);
        unitLengthAvg(g+1) = unitLength;
        decoded = [1 1];
        break
    elseif g == length(iois) - 2
        decoded = [];
        return
    end
end

prevDelay = 0;
for i = g+2:length(iois)
    delay = iois(i) + prevDelay;

    oneLength = ONE_ENCODE*unitLength;
    zeroLength = ZERO_ENCODE*unitLength;

    % Decode, pick closer and within threshold
    oneDist = abs(oneLength - delay);
    zeroDist = abs(zeroLength - delay);
    if oneDist < zeroDist && isWithinThresold(oneLength, delay)
        decoded = [decoded, 1];
        delay = delay / ONE_ENCODE;
    elseif isWithinThresold(zeroLength, delay)
        decoded = [decoded, 0];
        delay = delay / ZERO_ENCODE;
    else
        prevDelay = delay;
        continue
    end

    % Update unitLength, exponential moving average
    unitLength = unitLength*.2 + delay*.8;
    unitLengthAvg(i) = unitLength;
    prevDelay = 0;
end

if bPlot
    figure; stem(iois); title('Inter-onset Delays'); hold on
    stem(unitLengthAvg, 'r'); hold off;
    xlabel('Transient'); ylabel('Delay(samples)');
    legend('Inter-onset Delay', 'Unit Average');
    % divide zeros by zeros to turn them into NaNs so they don't get counted as a minimum
    minimum = log2(min([unitLengthAvg./unitLengthAvg.*unitLengthAvg iois]));
    figure; plot(log2(unitLengthAvg) - minimum, '-*r'); title('Inter onset delays'); hold on
    stem(log2(iois) - minimum, 'LineStyle', '-'); hold off;
    % figure; histogram(log2(iois), 20);
end

end


function withinThreshold = isWithinThresold(ioi1, ioi2)
    IOI_MAX_DIFF = 1.5;
    withinThreshold = (ioi1 / ioi2 < IOI_MAX_DIFF) && (ioi2 / ioi1 < IOI_MAX_DIFF);

end
