import csv
import sys

readpath = "./csv/yellow_tripdata_2015-01-06.csv"
writepath = "./csv/per_day/"

fieldnames='VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,pickup_longitude,pickup_latitude,RateCodeID,store_and_fwd_flag,dropoff_longitude,dropoff_latitude,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,total_amount'.split(",")

cnt=0

#------------------------------
def main():
    
    now_on = -1  #day counter
    now_writefile = ""
    datastack = []
    
    with open(readpath, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            pu_datetime = row["tpep_pickup_datetime"] #pick up datetime
            pu_day = int(pu_datetime[8:10])
            
            if pu_day != now_on:
                #dont write on first time
                if now_on != -1:
                    clearstack(datastack, now_writefile)
                now_on = pu_day
                now_writefile = writepath + "{}.csv".format(pu_datetime[:10])

            datastack.append(row)
            
            if len(datastack) > 10000:
                clearstack(datastack, now_writefile)

    clearstack(datastack, now_writefile)

    return

#------------------------------
def clearstack(lis, out):
    global cnt
    sys.stdout.write("\rwrite #{}, to {}".format(cnt, out))
    sys.stdout.flush()
    cnt += 1
    with open(out, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(lis)
    lis.clear()
    return

#------------------------------
if __name__ == "__main__":
    main()