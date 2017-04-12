filename='known.txt'

while read p; do
	id="$( cut -d ';' -f 1 <<< "$p" )"
    echo $p > $id.txt
done < $filename