function [H,R] = get_entropy(besedilo, p)
  % create mask for masking of non-alphanumeric symbols	
	mask = isalnum(besedilo);
  % convert all letters to uppercase
	proc_besedilo = toupper(besedilo(mask));
  % get unique letters
	unique_letters = unique(proc_besedilo);
  % count unique letters
  num_unique_letters = length(unique_letters);
	
	if (p == 0)
    % compute frequencies of letters and get probability of each letter
		P = histc(proc_besedilo, unique_letters)./length(proc_besedilo);
    % compute entropy
		H = -sum(P.*log2(P));
    % compute redundancy
		R = 1 - H/log2(26);
	end
	if (p == 1)
    % compute letter pairs in text
		pairs = [proc_besedilo, circshift(proc_besedilo, -1)];
    % remove pairs resulting from circshift functions use
    pairs = pairs(1:end-1, :);
    % get unique pairs and auxilliary vectors
		[U, I, J] = unique(pairs, "rows");
    % compute number of occurances of pairs
		num_pair = histc(J, [1:max(J)]);
    % compute probabilities of pairs
		P = num_pair./length(J);
    % compute entropy of pairs
	  H1 = -sum(P.*log2(P));
    % get entropy of single letters - recusive call
	  [H0, R0] = naloga1(besedilo, 0);
    % compute conditional entropy
    H = H1 - H0;
    % compute conditional redundancy
    R = 1 - H/log2(num_unique_letters);
  end
  if (p == 2)
    % compute triplets from text
    triplets = [proc_besedilo, circshift(proc_besedilo, -1), circshift(proc_besedilo, -2)];
    % remove triplets resulting from circshift function use
    triplets = triplets(1:end-2, :);
    % get unique triplets and auxilliary vectors
    [U, I, J] = unique(triplets, "rows");
    % compute number of occurances of each triplet
		num_triplets = histc(J, [1:max(J)]);
    % compute probabilities of triplets
		P = num_triplets./length(J);
    % compute entropy of triplets
	  H2 = -sum(P.*log2(P));
    % get entropy of pairs and single letters - recursive calls
    [H1, R1] = naloga1(besedilo, 1);
    [H0, R0] = naloga1(besedilo, 0);
    % compute conditional entropy
    H = H2 - (H1 + H0);
    % compute conditional redundancys
    R = 1 - H/log2(num_unique_letters);
	end
  if (p == 3)
    % compute quadruplets from text
    quadruplets = [proc_besedilo, circshift(proc_besedilo, -1), circshift(proc_besedilo, -2), circshift(proc_besedilo, -3)];
    % remove quadruplets resulting from circshift use
    quadruplets = quadruplets(1:end-3, :);
    % get unique quadruplets and auxilliary vectors
    [U, I, J] = unique(quadruplets, "rows");
    % compute number of occurances of each quadruplet
		num_quadruplets = histc(J, [1:max(J)]);
    % compute probabilities of quadrupletss
		P = num_quadruplets./length(J);
    % compute entropy of triplets
	  H3 = -sum(P.*log2(P));
    % get entropies for singletons, pairs and triplets
    [H2, R2] = naloga1(besedilo, 2);
    [H1, R1] = naloga1(besedilo, 1);
    [H0, R0] = naloga1(besedilo, 0);
    % compute conditional entropy
    H = H3 - (H1 + H2 + H0);
    % compute conditional redundancy
    R = 1 - H/log2(num_unique_letters);
	end

endfunction