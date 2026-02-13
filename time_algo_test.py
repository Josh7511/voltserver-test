
red_sequence = [1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,1,1]
blue_sequence = [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1,1]
green_sequence = [1,1,1,1,1,1,1,1,0,0,0,0,1,1,1]

fps = 30
red_list_list = [[]]
blue_list_list = [[]]
green_list_list = [[]]
red_time_sequence = []
blue_time_sequence = []
green_time_sequence = []
n = max(len(red_sequence), len(green_sequence), len(blue_sequence))

# split the sequences into lists of 1s and 0s, makes sure range doesn't go out of bounds
for i in range(n):
    if i > 0  and i < len(red_sequence) and ((red_sequence[i-1] == 0 and red_sequence[i] == 1 or red_sequence[i-1] == 1 and red_sequence[i] == 0)):
        red_list_list.append([])
    if i < len(red_sequence):
        red_list_list[-1].append(red_sequence[i])
    if i > 0 and i < len(blue_sequence) and ((blue_sequence[i-1] == 0 and blue_sequence[i] == 1 or blue_sequence[i-1] == 1 and blue_sequence[i] == 0)):
        blue_list_list.append([])
    if i < len(blue_sequence):
        blue_list_list[-1].append(blue_sequence[i])
    if i > 0 and i < len(green_sequence) and ((green_sequence[i-1] == 0 and green_sequence[i] == 1 or green_sequence[i-1] == 1 and green_sequence[i] == 0)):
        green_list_list.append([])
    if i < len(green_sequence):
        green_list_list[-1].append(green_sequence[i])

#calculate the time sequence for each list (can optimize this)
for i in range(len(red_list_list)):
    red_time_sequence.append(len(red_list_list[i]) / fps)
for i in range(len(blue_list_list)):
    blue_time_sequence.append(len(blue_list_list[i]) / fps)
for i in range(len(green_list_list)):
    green_time_sequence.append(len(green_list_list[i]) / fps)

print(red_time_sequence)
print(green_time_sequence)
print(blue_time_sequence)