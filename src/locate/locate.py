import os
import sys
import json
import argparse
import numpy as np
from dataset import prepare_dataset
from method import CNN, kNN, plot_pred, compute_error
import matplotlib.pyplot as plt
#from IPython import embed

parser = argparse.ArgumentParser(description="localization algorithm", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--train", type=str, required=True, help="training data list, NOTE the file format must be json string,\
                                                            \none sample per line,see data/train.txt and data/val.txt for reference")
parser.add_argument("--test", type=str, required=True, help="testing data list, NOTE as above")
parser.add_argument("--method", type=str, default="1NN", help="matching method/algorithm selection(default: 1NN)\
                    \n\txNN: nearest-neighbour using rssi, x is a integer indicating k in kNN\
                    \n\tCNN: convolution-neural-network using rssi")
parser.add_argument("--signal", type=str, default="mean", help="signal type used for matching(default: mean)\
                    \n\tmean: average value of RSSI sequence\n\tmedian: median value of RSSI sequence\
                    \n\tmax: max value of RSSI sequence\n\tmin: min value of RSSI sequence\
                    \n\tstd: standard deviation value of RSSI sequence\n\traw: raw RSSI sequence")
parser.add_argument("--weights_path", type=str, default=None, help="pretrained weights path for CNN model,\
                                                                    \nNOTE this must be given is using CNN")


def main(args):
    train_ds = prepare_dataset(args.train, args.signal)
    test_ds = prepare_dataset(args.test, args.signal)

    if args.method == "CNN":
        if args.weights_path is None:
            raise ValueError("invalid weights path {} for CNN".format(args.weights_path))
        # CNN
        locater = CNN(train_ds, args.weights_path)
    elif args.method.find("NN"):
        # kNN
        k = int(args.method[0:-2])
        locater = kNN(k, train_ds)
    else:
        raise ValueError("unknown method {}, use -h for details".format(args.method))

    true_coords = test_ds.pos
    pred_coords = locater(test_ds.ndary)
    print("True coords\n{}".format(true_coords))
    print("Pred coords\n{}".format(pred_coords))

    error = compute_error(true_coords, pred_coords)
    print("average error: {}".format(error))

    fig = plot_pred(train_ds, test_ds, pred_coords, "prediciton using {} with {}".format(args.method, args.signal))
    fig.show()
    while 1:
        c = input("save or not?[Y/N]")
        if c == "Y":
            name = input("input name for saved file")
            fig.savefig(name)
            break
        elif c == "N":
            break
        else:
            print("invalid input {}".format(c))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

    




