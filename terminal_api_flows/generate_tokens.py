import csv
import uuid

#
# This is just a utulity script to generate new tokens for the Terminal API until
# Edge Auth can support long lived JWT tokens or another solution becomes available
#
if __name__ == "__main__":
    with open('tokens.csv', 'w') as csv_file:
        uuidwriter = csv.writer(csv_file)

        #
        # Just change the range(x) value for how many you want written out
        # The resulting file contents is put into the
        # repository here: https://github.com/fivestars/websocket/pull/546/files
        #
        for i in range(1, 6):
            uuidwriter.writerow(['QADEMOBUSINESS{}'.format(i), uuid.uuid4().hex])

