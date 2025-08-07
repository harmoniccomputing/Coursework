import sys

def initialize_frequency(N):
  frequency = {}
  for state in range(1, N + 1):
    frequency[state] = 0
  return frequency

def run_dfa(N, S, X, machine): 
  current_state = S
  frequency = initialize_frequency(N)
  step = 0
  while step < X:
  #frequency[current_state] = frequency[current_state] + 1
    if current_state in machine:
      next_state = machine[current_state][0]
      temp_curr_state= current_state
      current_state = next_state
      frequency[temp_curr_state] += 1
    else:
      break
    step = step + 1   
  return frequency

def cycle_detection(N, S, X, machine):
  current_state = S
  visit = {}
  it = 0  # Position of head on input tape or at which step a cycle is detected
  frequency_counter = initialize_frequency(N)
  cycle = []

  while current_state not in visit and current_state in machine:
    visit[current_state] = it
    cycle.append(current_state)
    current_state = machine.get(current_state, [None])[0]
    it += 1

  if current_state not in visit or current_state is None:
    return run_dfa(N, S, X, machine) 
  
  cycle_start = visit[current_state]
  cycle_length = it - cycle_start

  if X <= cycle_start:
    return run_dfa(N, S, X, machine)
  else:
    pre_cycle_len = cycle_start 
    pre_cyc_freq = run_dfa(N, S, pre_cycle_len, machine)
    post_cycle_len = X - pre_cycle_len
    
    complete_cycles = post_cycle_len // cycle_length
    rem_tape = post_cycle_len % cycle_length

    cycle_freq = run_dfa(N, current_state, cycle_length, machine)
    rem_freq = run_dfa(N, current_state, rem_tape, machine)

    for i in range(1, N + 1):
      frequency_counter[i] = pre_cyc_freq[i] + (complete_cycles * cycle_freq[i]) + rem_freq[i]

    return frequency_counter

def build_machine():

  T = int(sys.stdin.readline().strip())
  #print(f"Total number of test cases: T={T}")
  test_case = []

  for i in range(1, T + 1):
    input_string = sys.stdin.readline().strip()
    components = input_string.split()
    N, M, S, X = map(int, components)
    test_case.append((N, M, S, X))

    #assert 1 <= N <= 10**5, "N must be between 1 and 100000"
    #assert 0 <= M <= 10**5, "M must be between 0 and 100000"
    #assert 1 <= S <= N, "S must be between 1 and N"
    #assert 0 <= X <= 10**12, "X must be between 0 and 10^12"
  #print(f"Test Case {i}: N={N}, M={M}, S={S}, X={X}")

    machine= {}
    for  j in range (1, M+1):
      transition_input = sys.stdin.readline().strip()
      from_state, to_state = map(int, transition_input.split())
      machine[from_state] = [to_state]  

    #for from_state in machine: 
    #  for to_state in machine[from_state]:
    #    print(from_state, "->", to_state)

    frequency = cycle_detection(N, S, X, machine)
    print(" ".join(str(frequency[i]) for i in range(1, N + 1)))


if __name__ == "__main__":
    build_machine()
