BEGIN { FS = ","; OFS = ","; }
NR == 1 { header = $0; next; }
{
    gsub(/"/, "", $4);  # Remove quotes from the 4th column
    filename = $4 ".csv";
    if (!seen[filename]++) {
        print header > filename;
    }
    print >> filename;
}
