## CloudFoundry Download Wrapper Build Pack

A CloudFoundry wrapper Build Pack that downloads your application files from a server and then runs the normal build pack.

This build pack takes a list of files, downloads them and then runs another build pack on those files.  This allows you to push a small list of files instead of the actual files themselves, saving bandidth and upload time.

## 30 Second Tutorial

Getting started with the build pack is easy.  With the cf command line utility installed, open a shell and follow these steps.

```bash
mkdir my-project
cd my-project
cat << EOF > download-list.txt
https://dl.dropboxusercontent.com/u/186123235/py-cf-buildpack-utils-tests/spring-music.war
EOF
cat << EOF > build-pack.txt
https://github.com/cloudfoundry/java-buildpack
EOF
cf push -m 512M -b https://github.com/dmikusa-pivotal/cf-download-build-pack --random-route spring-music-app
```

The example above will create and push a test application, `spring-music-app`, to CloudFoundry. The `-b` argument instructs CF to use this build pack. The remainder of the options and arguments are not specific to the build pack, for questions on those consult the output of cf `push -h`.

Here's the breakdown of what happens when you run the example above.

 - On your PC...
   - It'll create a new project directory.
   - In that folder, it'll create the two meta data files used by the build pack.  The first is the list of files to download.  The second is the build pack to actually use to run the app.
   - Run `cf push` to send the application to CloudFoundry.
 - On the server...
   - The build pack is executed
   - The list of files is downloaded (currently only supports HTTP/HTTPS)
   - The downloaded files are extracted to the applciation directory
   - The real build pack is run
   - Your application starts using the command specified by the real build pack

