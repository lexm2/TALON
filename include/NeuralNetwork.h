#ifndef NEURAL_NETWORK_H
#define NEURAL_NETWORK_H

#include <torch/torch.h>

class NeuralNetwork : public torch::nn::Module {
public:
    NeuralNetwork(int inputSize, int hiddenSize1, int hiddenSize2, int outputSize);
    torch::Tensor forward(torch::Tensor input);
private:
    torch::nn::Linear fc1{nullptr}, fc2{nullptr}, fc3{nullptr};
};

#endif