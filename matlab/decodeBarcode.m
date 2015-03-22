function decoded = decodeBarcode(trans, bPlot, Fs)

ONE_ENCODE = 1;
ZERO_ENCODE = 2;

% make sure there is something to decode
if length(trans) < 4 % 4 guard bits
    decoded = [];
    return
end

iois = diff(trans);

% For plotting purposes
unitLengthAvg = zeros(1,length(iois));

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

for i = g+2:length(iois)
    delay = iois(i);

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
        continue
    end

    % Update unitLength, exponential moving average
    unitLength = unitLength*.2 + delay*.8;
    unitLengthAvg(i) = unitLength;

end

if bPlot
    figure; stem(iois); title('Inter onset delays'); hold on
    stem(unitLengthAvg, 'r'); hold off;
end

end


function withinThreshold = isWithinThresold(ioi1, ioi2)
    IOI_MAX_DIFF = 1.5;
    withinThreshold = (ioi1 / ioi2 < IOI_MAX_DIFF) && (ioi2 / ioi1 < IOI_MAX_DIFF);

end
