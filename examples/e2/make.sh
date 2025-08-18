chasm make bar \
    --data d1.json \
    -m m1.chasm \
    -l l1.yaml \
    -o chart.svg

# Make it horizontal instead of vertical
chasm make bar \
    --data d1.json \
    -m m2.chasm \
    -l l1.yaml \
    -l l2.yaml \
    -o chart_h.svg

echo "## Example 2" >> ../examples.md
echo "![chart](./e2/chart.svg)" >> ../examples.md
echo "![charth](./e2/chart_h.svg)" >> ../examples.md
echo "" >> ../examples.md