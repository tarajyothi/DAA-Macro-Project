/*
 * DAA Macro Project - Unit II : Divide and Conquer / Greedy
 * Project 4 : Greedy Job Sequencing with Deadlines
 *
 * Problem : Each job takes 1 unit of time, has a deadline and a profit.
 *           A job earns its profit only if finished on or before its deadline.
 *           Choose and order jobs to maximise total profit.
 *
 * Greedy choice : always consider the job with the HIGHEST remaining profit and
 *           put it in the LATEST free slot that is <= its deadline. Using the
 *           latest slot keeps earlier slots free for other tight-deadline jobs.
 *
 * Build : g++ -std=c++17 -o Project4_JobSequencing Project4_JobSequencing.cpp
 * Run   : ./Project4_JobSequencing
 */
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Job {
    string id;
    int deadline;
    int profit;
};

int main() {
    vector<Job> jobs = {
        {"J1", 2, 100}, {"J2", 1, 19}, {"J3", 2, 27}, {"J4", 1, 25}, {"J5", 3, 15}};

    cout << "=== Greedy Job Sequencing with Deadlines ===\n\nInput jobs:\n";
    cout << "Job  Deadline  Profit\n";
    for (const Job &j : jobs)
        cout << j.id << "   " << j.deadline << "         " << j.profit << "\n";

    // Step 1: sort by profit, highest first  -> O(n log n)
    sort(jobs.begin(), jobs.end(),
         [](const Job &a, const Job &b) { return a.profit > b.profit; });

    cout << "\nStep 1: Jobs sorted by decreasing profit:\n";
    for (const Job &j : jobs)
        cout << "  " << j.id << " (deadline " << j.deadline << ", profit " << j.profit << ")\n";

    int maxDeadline = 0;
    for (const Job &j : jobs) maxDeadline = max(maxDeadline, j.deadline);

    vector<string> slot(maxDeadline + 1, "");  // slot[t] = job run in time slot t (1-indexed)
    int totalProfit = 0, scheduled = 0;

    cout << "\nStep 2: Greedy selection (latest free slot <= deadline):\n";
    for (const Job &j : jobs) {                 // Step 3: O(n * D) slot search
        int t = min(maxDeadline, j.deadline);
        while (t >= 1 && !slot[t].empty()) t--; // move left until a free slot is found
        if (t >= 1) {
            slot[t] = j.id;
            totalProfit += j.profit;
            scheduled++;
            cout << "  " << j.id << ": slot " << t << " is free -> SCHEDULE (profit +" << j.profit << ")\n";
        } else {
            cout << "  " << j.id << ": no free slot <= deadline " << j.deadline << " -> SKIP\n";
        }
    }

    cout << "\nFinal schedule:\n";
    for (int t = 1; t <= maxDeadline; t++)
        cout << "  Slot " << t << " : " << (slot[t].empty() ? "(idle)" : slot[t]) << "\n";

    cout << "\nSelected jobs : ";
    for (int t = 1; t <= maxDeadline; t++) if (!slot[t].empty()) cout << slot[t] << " ";
    cout << "\nJobs scheduled: " << scheduled << " of " << jobs.size();
    cout << "\nTotal profit  : " << totalProfit << "\n";

    cout << "\nWhy greedy works: taking the most profitable job first and placing it as late as\n"
            "possible never blocks a better option, because every earlier slot stays free for\n"
            "jobs with tighter deadlines.\n";
    return 0;
}
