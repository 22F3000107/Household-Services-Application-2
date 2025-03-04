export default {
    template: `
    <div>
        <h2>Update Job Status</h2>
        <ul>
            <li v-for="job in jobs" :key="job.id">
                {{ job.service }} - Status: {{ job.status }}
                <button @click="updateStatus(job.id, 'In Progress')">In Progress</button>
                <button @click="updateStatus(job.id, 'Completed')">Completed</button>
            </li>
        </ul>
    </div>
    `,
    data() {
        return {
            jobs: [
                { id: 1, service: "AC Repair", status: "Pending" },
                { id: 2, service: "Cleaning", status: "In Progress" }
            ]
        };
    },
    methods: {
        updateStatus(jobId, newStatus) {
            alert(`Job ${jobId} updated to ${newStatus}.`);
        }
    }
};
