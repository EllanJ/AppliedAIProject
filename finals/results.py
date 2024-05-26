import matplotlib.pyplot as plt



labels = ['Correct', 'Incorrect']
values = [90, 10]

plt.bar(labels, values, color=['green', 'red'])
plt.title('Voice Recognition Accuracy')
plt.xlabel('Recognition Result')
plt.ylabel('Number of Commands')
plt.show()


command_types = ['Play Song', 'Weather Info', 'Answer Query', 'AI Answers']
response_times = [3, 5.5, 4, 7.5]

plt.plot(command_types, response_times, marker='o')
plt.title('Response Time Analysis')
plt.xlabel('Command Type')
plt.ylabel('Average Response Time (seconds)')
plt.show()




error_types = ['Voice Recognition', 'Wikipedia Retrieval', 'Opening Applications']
error_counts = [10, 5, 3]

plt.bar(error_types, error_counts, color='orange')
plt.title('Error Analysis')
plt.xlabel('Error Type')
plt.ylabel('Frequency')
plt.show()
