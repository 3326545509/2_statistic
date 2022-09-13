coldfile=$1   #'cold.txt'
sacdatafile=$2    #'all_withcold.csv'
outfile=$3    #'all.csv'

#----新建文档 插入表头
cat $sacdatafile|awk -F '' '{if(NR=='1')print}'>$outfile

imax=`cat $sacdatafile|wc -l`
jmax=`cat $coldfile|wc -l`
i=2 #----i=1是表头
j=1
while (($i<=$imax ))
do
sacstation=`cat $sacdatafile|awk -F ',' '{if(NR=='$i')print$1}'`

j=1
#-----judge=1: 不是有问题station =0: 为有问题台站
judge=1
while (($j<=$jmax ))
do
coldstation=`cat $coldfile|awk -F '' '{if(NR=='$j')print}'`
#echo "$sacstation $coldstation $i $j"
if [ ${sacstation} == ${coldstation} ]
then
    judge=0
    #echo "$i"
    break
else
    let j++
fi
done

if [ $judge == 1 ]
then
    cat $sacdatafile|awk -F '' '{if(NR=='$i')print}'>>$outfile
fi

let i++
done