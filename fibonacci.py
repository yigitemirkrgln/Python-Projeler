n=int(input("Kaç eleman: "))
f=[0,1]
for i in range(2,n): f.append(f[-1]+f[-2])
print(f)
