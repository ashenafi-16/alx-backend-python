# Jenkins Setup Guide for Django Messaging App

## 1. Run Jenkins in Docker Container

Execute the following command to start Jenkins:

```bash
docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

**What this command does:**
- Pulls the latest LTS Jenkins image
- Exposes Jenkins on port 8080 (web interface)
- Exposes port 50000 for Jenkins agents
- Maps Jenkins home directory to persist data
- Maps Docker socket for Docker operations

## 2. Access Jenkins Dashboard

1. Open your browser and go to `http://localhost:8080`
2. Wait for Jenkins to start up (may take a few minutes)
3. Get the initial admin password:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

## 3. Install Required Plugins

After initial setup, install these plugins:

### **Git Plugin**
- Go to **Manage Jenkins** → **Manage Plugins** → **Available**
- Search for "Git plugin" and install
- Restart Jenkins when prompted

### **Pipeline Plugin**
- Search for "Pipeline" and install
- Includes: Pipeline, Pipeline: API, Pipeline: Basic Steps, etc.

### **ShiningPanda Plugin**
- Search for "ShiningPanda" and install
- Provides Python support for Jenkins

### **Additional Recommended Plugins**
- **Docker Plugin**: For Docker operations
- **Credentials Plugin**: For storing secrets
- **HTML Publisher Plugin**: For test reports
- **JUnit Plugin**: For test results
- **Cobertura Plugin**: For coverage reports

## 4. Configure Jenkins Credentials

### **GitHub Credentials**
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **System** → **Global credentials** → **Add Credentials**
3. Choose **SSH Username with private key** or **Username with password**
4. **ID**: `github-credentials` (this must match the credentialsId in Jenkinsfile)
5. **Username**: Your GitHub username
6. **Password/Private Key**: Your GitHub password or SSH private key
7. **Description**: GitHub credentials for messaging app repository

### **Docker Hub Credentials**
1. Add new credentials
2. Choose **Username with password**
3. ID: `docker-hub-credentials`
4. Username: Your Docker Hub username
5. Password: Your Docker Hub access token

## 5. Create Jenkins Pipeline

### **Option 1: Create from SCM (Recommended)**
1. Click **New Item**
2. Enter name: `messaging-app-pipeline`
3. Choose **Pipeline**
4. In **Pipeline** section, choose **Pipeline script from SCM**
5. SCM: **Git**
6. Repository URL: Your GitHub repo URL
7. Credentials: Select your GitHub credentials
8. Branch: `*/main`
9. Script Path: `messaging_app/Jenkinsfile`

### **Option 2: Create from Pipeline Script**
1. Click **New Item**
2. Enter name: `messaging-app-pipeline`
3. Choose **Pipeline**
4. In **Pipeline** section, paste the Jenkinsfile content

## 6. Configure Pipeline Environment

### **Update GitHub Repository URL**
In the `Jenkinsfile`, update the repository URL to match your actual GitHub repository:

```groovy
userRemoteConfigs: [[
    url: 'https://github.com/YOUR-ACTUAL-USERNAME/alx-backend-python.git',  // Change this!
    credentialsId: 'github-credentials'
]]
```

### **Update Docker Registry**
Update the `Jenkinsfile` environment variables:

```groovy
environment {
    DOCKER_IMAGE = 'messaging-app'
    DOCKER_TAG = "${env.BUILD_NUMBER}"
    DOCKER_REGISTRY = 'your-actual-dockerhub-username'  // Change this!
    PYTHON_VERSION = '3.10'
}
```

## 7. Run the Pipeline

1. Go to your pipeline
2. Click **Build Now**
3. Monitor the build logs
4. Check build results and artifacts

## 8. View Results

### **Test Results**
- Go to build → **Test Results**
- View pytest results and coverage

### **Coverage Reports**
- Go to build → **Coverage Report**
- View HTML coverage reports

### **Build Artifacts**
- Go to build → **Artifacts**
- Download test results and reports

## 9. Troubleshooting

### **Common Issues**

#### **Permission Denied for Docker**
```bash
# Add jenkins user to docker group
docker exec jenkins usermod -aG docker jenkins
docker restart jenkins
```

#### **Python Virtual Environment Issues**
- Ensure Python 3.10+ is available in Jenkins container
- Check PATH and Python installation

#### **Git Authentication Issues**
- Verify GitHub credentials are correct
- Check SSH key permissions if using SSH

#### **Docker Build Failures**
- Ensure Docker socket is properly mounted
- Check Docker Hub credentials
- Verify Dockerfile exists in repository

### **Logs and Debugging**
- Check Jenkins system logs: **Manage Jenkins** → **System Log**
- View build console output for detailed error messages
- Check Jenkins home directory for configuration issues

## 10. Security Considerations

1. **Change default admin password**
2. **Use Jenkins security features**
3. **Limit Docker access**
4. **Regular plugin updates**
5. **Backup Jenkins home directory**

## 11. Next Steps

After successful setup:
1. **Automate pipeline triggers** (webhooks, polling)
2. **Set up notifications** (email, Slack, etc.)
3. **Configure deployment environments**
4. **Add security scanning**
5. **Set up monitoring and alerting**

## 12. Useful Commands

```bash
# Check Jenkins status
docker ps | grep jenkins

# View Jenkins logs
docker logs jenkins

# Restart Jenkins
docker restart jenkins

# Backup Jenkins data
docker run --rm -v jenkins_home:/data -v $(pwd):/backup alpine tar czf /backup/jenkins-backup.tar.gz -C /data .

# Restore Jenkins data
docker run --rm -v jenkins_home:/data -v $(pwd):/backup alpine tar xzf /backup/jenkins-backup.tar.gz -C /data
```

## 13. GitHub Actions Integration

The repository also includes GitHub Actions workflows:
- **`.github/workflows/ci.yml`**: Runs tests and code quality checks
- **`.github/workflows/dep.yml`**: Builds and deploys Docker images

These can run alongside or as an alternative to Jenkins pipelines.
