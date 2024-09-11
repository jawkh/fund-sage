import { debug } from "console";

export const config = {
  vpc: {
    cidr: '172.16.0.0/24', // CIDR block for the VPC
    maxAzs: 2, // Maximum number of Availability Zones
    natGateways: 1, // Number of NAT Gateways
  },
  database: {
    minCapacity: 2, // Minimum Aurora Capacity Units (ACU), valid range starts from 2
    maxCapacity: 8, // Maximum ACU (can be 2, 4, 8, 16, etc.)
    autoPauseMinutes: 5, // Auto-pause after 5 minutes of inactivity
  },
  apiGateway: {
    throttlingRateLimit: 1000, // Maximum request rate (per second) before throttling
    throttlingBurstLimit: 500, // Maximum burst requests allowed
    usagePlanRateLimit: 100, // API usage plan rate limit (per second)
    usagePlanBurstLimit: 200, // API usage plan burst limit
  },
  ecs: {
    cpu: 256, // CPU units for ECS service
    memoryLimitMiB: 512, // Memory limit for ECS service (in MiB)
    minCapacity: 1, // Minimum number of ECS tasks
    maxCapacity: 2, // Maximum number of ECS tasks
    targetCpuUtilization: 70, // Target CPU utilization percentage for scaling
  },
  app: {
    flask_debug: false, // Enable or disable Flask debug mode
    debugpy_host: '0.0.0.0', // Host for debugpy
    debugpy_port: 5678, // Port for debugpy
    flaskApp: 'api/__init__.py', // Flask app entry point
    flaskRunHost: '0.0.0.0', // Host for running Flask app
    flaskRunPort: 5000, // Port for Flask app
    flaskEnv: 'development', // Flask environment (development, production, etc.)
    secretKey: 'change-this-in-production', // Secret key for Flask app (change in production)
    jwtSecretKey: 'change-this-in-production', // Secret key for JWT (change in production)
    jwtAccessTokenExpires: 3600, // JWT access token expiration time (in seconds)
    serverName: 'your-server-name', // Server name for the Flask app
    applicationRoot: '/', // Root URL for the application
    preferredUrlScheme: 'https', // Preferred URL scheme (http/https)
    maxPasswordRetries: 5, // Maximum allowed password retries
    passwordRetriesTimeWindowMinutes: 15, // Time window for password retry limit (in minutes)
    flaskDebug: false, // Enable or disable Flask debug mode
    provisionDummyApplications: true, // Provision dummy applications for testing
    provisionDummyApplicants: true, // Provision dummy applicants for testing
  },
};
