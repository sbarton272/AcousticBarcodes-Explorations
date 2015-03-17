function decoded = decodeBarcode(trans, bPlot);

ONE_ENCODE = 1;
ZERO_ENCODE = 2;

interOnsetDelay = diff(trans);

% Decide if interonset delay is encoding 0 or 1 based on which multiple of
% unitLen it is closer to
unitLength = interOnsetDelay(1); % Assume first is unit len
decoded = [1];
% For plotting purposes
unitLengthAvg = zeros(1,length(interOnsetDelay));
unitLengthAvg(1) = unitLength;
for i = 2:length(interOnsetDelay)
    delay = interOnsetDelay(i);
    
    % Decode, pick closer
    oneDist = abs(ONE_ENCODE*unitLength - delay);
    zeroDist = abs(ZERO_ENCODE*unitLength - delay);
    if oneDist < zeroDist
        decoded = [decoded, 1];
        delay = delay / ONE_ENCODE;
    else
        decoded = [decoded, 0];
        delay = delay / ZERO_ENCODE;
    end
    
    % Update unitLength, exponential moving average
    unitLength = unitLength*.2 + delay*.8;
    unitLengthAvg(i) = unitLength;
    
end

if bPlot
    figure; stem(interOnsetDelay); title('Inter onset delays'); hold on
    stem(unitLengthAvg, 'r'); hold off;
end
end