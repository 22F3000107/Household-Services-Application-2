export default {
    template: `
    <div>
        <h2>My Service Requests</h2>
        <ul>
            <li v-for="request in requests" :key="request.id">
                {{ request.service }} - Status: {{ request.status }}
            </li>
        </ul>
    </div>
    `,
    data() {
        return {
            requests: [
                { id: 1, service: "AC Repair", status: "Pending" },
                { id: 2, service: "Cleaning", status: "Completed" }
            ]
        };
    }
};
