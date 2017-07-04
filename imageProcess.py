import argparse






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp', type=str, default='/home/theo/Dropbox/TER/Images/bar chart/',
                        help='Directory for storing input data')
    parser.add_argument('--out', type=str, default='/home/theo/temp/la/',
                        help='Directory for storing output data')
    parser.add_argument('--ext', type=str, default='jpg',
                        help='Extention for output data')
    parser.add_argument('--size', type=int, default=100,
                        help='Size for output data')
    FLAGS, unparsed = parser.parse_known_args()
    main()
