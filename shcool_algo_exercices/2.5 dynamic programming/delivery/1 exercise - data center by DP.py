class Graph():

    def __init__(self, stages, rsc):
        self.STAGES    = stages
        self.RESOURCES = rsc
        self.val_f     = [[0 for column in range(rsc + 1)] for row in range(stages)]
        self.rsc_taken = [[0 for column in range(rsc + 1)] for row in range(stages)]

        for i in range(stages):
            for j in range(len(self.val_f[0])):
                self.val_f[i][j] = -1  # Initialize values to -1 to denote "not yet computed"

    def reward(self, activity, rsc):
        if rsc > 0:
            if activity == 0:
                return 7 * rsc + 2
            if activity == 1:
                return 3 * rsc + 7
            if activity == 2:
                return 4 * rsc + 5
        else:
            return 0

    def f(self, stage, avail_rsc):
        # Base case: If we're at the last stage, return 0 as there's no further reward
        if stage == self.STAGES - 1:
            return 0

        # If already computed, return the stored value
        if self.val_f[stage][avail_rsc] != -1:
            return self.val_f[stage][avail_rsc]

        max_reward = 0
        best_rsc = 0

        # Iterate over all possible resources that can be allocated at this stage
        for rsc_taken in range(avail_rsc + 1):
            current_reward = self.reward(stage, rsc_taken)
            future_reward = self.f(stage + 1, avail_rsc - rsc_taken)
            total_reward = current_reward + future_reward

            # Update maximum reward if we find a better allocation
            if total_reward > max_reward:
                max_reward = total_reward
                best_rsc = rsc_taken

        # Store the result in the table
        self.val_f[stage][avail_rsc] = max_reward
        self.rsc_taken[stage][avail_rsc] = best_rsc

        return max_reward


if __name__ == "__main__":

    stages    = 4
    resources = 6

    g = Graph(stages, resources)

    reward = g.f(0, 6)

    print("\nResultant f(stage, avail_rsc):")
    for stage in range(g.STAGES-1):
        print(g.val_f[stage])

    stage     = 0
    avail_rsc = 6

    print("\nMax reward: ", reward)
    for activity in range(g.STAGES-1):
        rsc_taken = g.rsc_taken[stage][avail_rsc]
        print("Activity:", activity, ", Resources taken:", rsc_taken)
        stage += 1
        avail_rsc -= rsc_taken
