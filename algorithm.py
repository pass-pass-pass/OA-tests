def check_parentheses(strings):
    # 内嵌函数用来处理每一行的数据
    def mark_unmatched(s):
        stack = []
        output = [' '] * len(s) # 存储答案

        # 遍历string
        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)  # 把 ‘（’ 的index推进stack
            elif char == ')':
                if stack:
                    stack.pop()  # 把”（“ 的index从stack中推出来因为我们找到了匹配
                else:
                    output[i] = '?'  # 如果没有找到匹配的”）“ 这个index我们记为？

            

        # 把剩下的没有匹配的”（” 记为x
        for idx in (stack):
            output[idx] = 'x'
        
        return ''.join(output)  # 把list变成string
    
    ans = []
    # 遍历每一行的string, 用我们的内嵌函数生成答案
    for str in (strings):
        #加入 原string
        ans.append(str)
        #加入 我们替换之后的string
        ans.append(mark_unmatched(str) )
    return ans

# 案例
sample_input = [
    "bge)))))))))",
    "((IIII)))))",
    "()()()()(uuu",
    "))))UUUU((()"
]

# call这个函数
output = check_parentheses(sample_input)

# 打印输出
for line in output:
    print(line)



