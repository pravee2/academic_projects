%**************************************************************************
% Name: Varun Praveen
% CUID: pravee2
% Course: ECE-8720
% Assignment Number: Takehome 2 : case 3
%**************************************************************************

clc;
clear all;
close all;

% this section of the code is for normalizing the data.
% data_AEP_prenorm = load('data_AEP.txt','-ascii');
% data_nonAEP_prenorm = load('data_nonAEP.txt','-ascii');
% totalAEP = length(data_AEP_prenorm);
% totalNonAEP = length(data_nonAEP_prenorm);
% concatenated_Data = [data_AEP_prenorm;data_nonAEP_prenorm];
%
% for i=1:length(concatenated_Data)
%     concatenated_Data_norm(i,:) = (concatenated_Data(i,:)-min(concatenated_Data))./...
%         (max(concatenated_Data)-min(concatenated_Data));
% end
%
% data = concatenated_Data_norm(1:totalAEP,:);
% data_nonAEP = concatenated_Data_norm(totalAEP+1:totalAEP+totalNonAEP,:);

data = load('data_AEP.txt','-ascii');
data_nonAEP = load('data_nonAEP.txt','ascii');
% class_count = min(length(data),length(data_nonAEP));
% concat =  [data(1:class_count,:);data_nonAEP(1:class_count,:)];
[concat, concat_validate, class_count, testcount] = near_miss(data,data_nonAEP);
labels = [ones(class_count,1) -ones(class_count,1); -ones(class_count,1) ones(class_count,1)];
index = zeros(class_count*2,1);

labels_test = [ones(testcount,1) -ones(testcount,1); -ones(testcount,1) ones(testcount,1)];
for i=1:class_count
    index(2*(i-1)+1) = i;
    index(2*(i-1)+2) = class_count + i;
end

N = size(data);
d = N(2);
H = 2*d+1;                                            %hidden layer count
epsilon = 0.00000001;                                      %learning rate of ANN
c = 2;

weights_H = -0.0005+rand(d+1,H)*(0.001);
weights_O = -0.05+rand(H+1,c)*0.1;

AEPcount = 0;
NONAEPcount = 0;
for i=1:length(index)                             %shuffling data and
    data_in_norm(i,:) = concat(index(i),:);            %respective target output
    target_out(i,:) = labels(index(i),:);
    if(index(i)>class_count)
        NONAEPcount = NONAEPcount + 1;
    else
        AEPcount = AEPcount + 1;
    end
end

% first pass
data_in_norm = [data_in_norm ones(length(data_in_norm),1)];
data_test_norm = [concat_validate ones(length(concat_validate),1)];
iteration_ROM = 1;
updatecount = 0;
%*********************     Random Optimization     ************************
while(iteration_ROM < 100)
    Net_H = data_in_norm*weights_H;
    output_H = tanh(Net_H);
    
    output_H = [output_H ones(length(output_H),1)];
    Net_O = output_H * weights_O;
    output_O = tanh(Net_O);
    
    Error(iteration_ROM) = 0.5 * sum(norm(target_out - output_O).^2);
    eofK = -0.00005+randn(d+1,H)*0.0001;
    eofKO = -0.005 + randn(H+1,c) * 0.01;
    
    weights_H_updated = weights_H + eofK;
    weights_O_updated = weights_O + eofKO;
    
    Net_H = data_in_norm*weights_H_updated;
    output_H = tanh(Net_H);
    
    output_H = [output_H ones(length(output_H),1)];
    Net_O = output_H * weights_O_updated;
    output_O = tanh(Net_O);
    
    Error_updated(iteration_ROM) = 0.5 * sum(norm(target_out - output_O).^2);
    
    if(Error_updated(iteration_ROM) < Error(iteration_ROM))
        weights_H = weights_H_updated;
        weights_O = weights_O_updated;
        updatecount = updatecount + 1;
    else
        weights_H_updated = weights_H - eofK;
        weights_O_updated = weights_O - eofKO;
        Net_H = data_in_norm*weights_H_updated;
        output_H = tanh(Net_H);
        
        output_H = [output_H ones(length(output_H),1)];
        Net_O = output_H * weights_O_updated;
        output_O = tanh(Net_O);
        Error_updated(iteration_ROM) = 0.5 * sum(norm(target_out - output_O).^2);
        if(Error_updated(iteration_ROM) < Error(iteration_ROM))
            weights_H = weights_H_updated;
            weights_O = weights_O_updated;
            updatecount = updatecount + 1;
        end
    end
    iteration_ROM = iteration_ROM + 1;
end

dlmwrite('case3_hidden.txt',weights_H);
dlmwrite('case3_output.txt',weights_O);

updatecount
figure(1)
plot(Error,'k');
grid;
xlabel('iterations');
ylabel('TSS');


% ***************************         ANN         *************************
iteration = 1;

while(iteration<100001)
    %     Net_H = data_in*weights_H;
    Net_H = data_in_norm*weights_H;
    output_H = tanh(Net_H);
    %     output_H = 1./(1+exp(-Net_H));
    
    % ******************            OUTPUT LAYER            *******************
    output_H = [output_H ones(length(output_H),1)];
    Net_O = output_H * weights_O;
    output_O = tanh(Net_O);
    
    % ***************           BACK - PROPOGATION          *******************
    
    error_O = target_out - output_O;
    output_delta = error_O.*(1-(output_O).^2);
    weightcorr_hidden = epsilon * (output_H' * output_delta);
    
    hidden_delta = (1-(output_H).^2).*(output_delta* weights_O');
    weightcorr_input = epsilon .* data_in_norm' * hidden_delta;
    
    
    weights_O = weights_O + weightcorr_hidden;
    weights_H = weights_H + weightcorr_input(:,1:H);
    
    error_measure(iteration) = 1/2 * sum(norm(error_O)^2);
    iteration = iteration + 1;
end

figure(2);
plot(error_measure,'k');
grid;
xlabel('iterations');
ylabel('TSS');

% ********      computing confusion matrix for training data       ********
Net_H = data_in_norm*weights_H;
output_H = tanh(Net_H);

output_H = [output_H ones(length(output_H),1)];
Net_O = output_H * weights_O;
output_O = tanh(Net_O);

confusion_matrix_train = zeros(c,c);
correct_count = 0;
for i=1:length(index)
    if(target_out(i,1)==1)
        if(output_O(i,1) > 0)
            confusion_matrix_train(1,1) = confusion_matrix_train(1,1) + 1;
            correct_count = correct_count + 1;
        elseif(output_O(i,1) < 0)
            confusion_matrix_train(1,2) = confusion_matrix_train(1,2) + 1;
        end
    elseif(target_out(i,2)== 1)
        if(output_O(i,2) > 0)
            confusion_matrix_train(2,2) = confusion_matrix_train(2,2) + 1;
            correct_count = correct_count + 1;
        elseif(output_O(i,2) < 0)
            confusion_matrix_train(2,1) = confusion_matrix_train(2,1) + 1;
        end
    end
end
fprintf('Confusion Matrix: ');
confusion_matrix_train
fprintf('Total classification error percentage : %0.4f\n', correct_count/...
    (class_count*2));

% *********************           Testing Network         *****************


Net_H = data_test_norm*weights_H;
output_H = tanh(Net_H);
count = size(output_H);
output_H = [output_H ones(count(1),1)];
Net_O = output_H * weights_O;
output_O = tanh(Net_O);

confusion_matrix_test = zeros(c,c);
correct_count_test = 0;


for i=1:testcount*2
    if(labels_test(i,1)==1)
        if(output_O(i,1) > 0)
            confusion_matrix_test(1,1) = confusion_matrix_test(1,1) + 1;
            correct_count_test = correct_count_test + 1;
        elseif(output_O(i,1) < 0)
            confusion_matrix_test(1,2) = confusion_matrix_test(1,2) + 1;
        end
    elseif(labels_test(i,2)== 1)
        if(output_O(i,2) > 0)
            confusion_matrix_test(2,2) = confusion_matrix_test(2,2) + 1;
            correct_count_test = correct_count_test + 1;
        elseif(output_O(i,2) < 0)
            confusion_matrix_test(2,1) = confusion_matrix_test(2,1) + 1;
        end
    end
end
fprintf('Confusion Matrix: ');
confusion_matrix_test
sensitivity = confusion_matrix_test(1,1)/testcount
specificity = confusion_matrix_test(2,2)/testcount
fprintf('Total classification error percentage : %0.4f\n', correct_count_test/...
    (testcount*2));



% Testing for ALL NON AEP Data samples
labels_NonAEP = [-ones(length(data_nonAEP),1) ones(length(data_nonAEP),1)];
data_NonAEP = [data_nonAEP ones(length(data_nonAEP),1)];
Net_H = data_NonAEP*weights_H;
output_H = tanh(Net_H);
count = size(output_H);
output_H = [output_H ones(count(1),1)];
Net_O = output_H * weights_O;
output_O = tanh(Net_O);

confusion_matrix_test_nonAEP = zeros(c,c);
correct_count_test_nonAEP = 0;


for i=1:length(data_nonAEP)
    if(labels_NonAEP(i,1)==1)
        if(output_O(i,1) > 0)
            confusion_matrix_test_nonAEP(1,1) = confusion_matrix_test_nonAEP(1,1) + 1;
            correct_count_test_nonAEP = correct_count_test_nonAEP + 1;
        elseif(output_O(i,1) < 0)
            confusion_matrix_test_nonAEP(1,2) = confusion_matrix_test_nonAEP(1,2) + 1;
        end
    elseif(labels_NonAEP(i,2)== 1)
        if(output_O(i,2) > 0)
            confusion_matrix_test_nonAEP(2,2) = confusion_matrix_test_nonAEP(2,2) + 1;
            correct_count_test_nonAEP = correct_count_test_nonAEP + 1;
        elseif(output_O(i,2) < 0)
            confusion_matrix_test_nonAEP(2,1) = confusion_matrix_test_nonAEP(2,1) + 1;
        end
    end
end
fprintf('Confusion Matrix: ');
confusion_matrix_test_nonAEP
fprintf('Total classification error percentage : %0.4f\n', correct_count_test_nonAEP/...
    (length(data_NonAEP)));

