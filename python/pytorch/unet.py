# -*- coding=utf-8 -*-
import einops.layers.torch as elt
import torch


class Unet(torch.nn.Module):
    def __init__(self):

        super(Unet, self).__init__()

        # 模块化结构，这也是后面常用到的模型结构

        self.first_block_down = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
            torch.nn.GELU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.second_block_down = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            torch.nn.GELU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.latent_space_block = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            torch.nn.GELU(),
        )

        self.second_block_up = torch.nn.Sequential(
            torch.nn.Upsample(scale_factor=2),
            torch.nn.Conv2d(in_channels=128, out_channels=64, kernel_size=3, padding=1),
            torch.nn.GELU(),
        )

        self.first_block_up = torch.nn.Sequential(
            torch.nn.Upsample(scale_factor=2),
            torch.nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3, padding=1),
            torch.nn.GELU(),
        )

        self.convUP_end = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=32, out_channels=1, kernel_size=3, padding=1), torch.nn.Tanh()
        )

    def forward(self, img_tensor):

        image = img_tensor

        image = self.first_block_down(image)

        # print(image.shape)

        # torch.Size([5, 32, 14, 14])

        image = self.second_block_down(image)

        # print(image.shape)

        # torch.Size([5, 16, 7, 7])

        image = self.latent_space_block(image)

        # print(image.shape)

        # torch.Size([5, 8, 7, 7])

        image = self.second_block_up(image)

        # print(image.shape)

        # torch.Size([5, 16, 14, 14])

        image = self.first_block_up(image)

        # print(image.shape)

        # torch.Size([5, 32, 28, 28])

        image = self.convUP_end(image)

        # print(image.shape)

        # torch.Size([5, 32, 28, 28])

        return image


if __name__ == '__main__':  # main是Python进行单文件测试的技巧，请读者记住这种写法

    image = torch.randn(size=(5, 1, 28, 28))
    print(f"{image=}")

    Unet()(image)
