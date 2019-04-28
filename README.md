# CS6460
This is the python and helm chart definition for my project JupyterAssessor for CS6460.
This uses interacts with the code in [jupyter-spawner](https://github.com/zach-schoenberger/jupyter-spawner) to dynamically spin up testing pods for JupyterHub.

## Setup 
First setup `kubectl` to connect to your kubernetes cluster. This depends on your cloud provider or kubernetes setup. An example can be found [here](https://cloud.google.com/kubernetes-engine/docs/quickstart).
Then checkout the repository and change directories. 
```
git clone https://github.com/zach-schoenberger/CS6460
cd ./CS6460
```
Then run the `helm-install.sh` script to install the helm charts.
```
./helm-install.sh
```

You should now be able to run `kubectl --namespace jhub get svc` and get an output that looks like:
```
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)                      AGE
hub               ClusterIP      10.47.244.40    <none>           8081/TCP                     21d
jupyter-spawner   ClusterIP      10.47.240.248   <none>           80/TCP                       21d
proxy-api         ClusterIP      10.47.253.14    <none>           8001/TCP                     21d
proxy-public      LoadBalancer   10.47.253.103   34.66.49.226     80:30560/TCP,443:31998/TCP   21d
redis-master      LoadBalancer   10.47.240.132   35.224.232.159   6379:32590/TCP               40d
redis-slave       ClusterIP      10.47.253.0     <none>           6379/TCP                     40d
```
You should see at least all of the services above. Once the environment has finished spinning up, the `EXTERNAL-IP` of `proxy-public` is the ip to be for the JupyterHub login.


## Customization
### Notebook Container
To customize the container that runs the notebooks, modifications should be made to the `jhub-spawner-client/jhub.Dockerfile`. This is where packages should be added or removed, along with any other changes. If there is a default set of files that should be made available this is where to do it. The change the `build.sh` file to tag the new image with your image tag. Then modify the `jhub-config.yml` file to use the new image that was created. The `singleuser` and `spawner` image configs should be updated to use the new image.

### Assessor Customization
This is the aspect that teachers always need to customize. To customize the assessor, the teacher should modify the python script that is used to run the students submissions to assess and grade them. Inside [jupyter-spawner](https://github.com/zach-schoenberger/jupyter-spawner) the file `createAssessor.sh` is used to load the assessor python file into Kubernetes as a `configmap`. There is an example default script in the repository called `defaultPyscriptAssessor.py` that simply runs the submitted script.