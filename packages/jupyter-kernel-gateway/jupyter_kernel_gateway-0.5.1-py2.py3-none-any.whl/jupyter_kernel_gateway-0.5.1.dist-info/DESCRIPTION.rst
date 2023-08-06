Jupyter Kernel Gateway is a web server that supports different mechanisms for
spawning and communicating with Jupyter kernels, such as:

* A Jupyter Notebook server-compatible HTTP API used for requesting kernels
  and talking the `Jupyter kernel protocol <https://jupyter-client.readthedocs.org/en/latest/messaging.html>`_
  with the kernels over Websockets
* A HTTP API defined by annotated notebook cells that maps HTTP verbs and
  resources to code to execute on a kernel

The server launches kernels in its local process/filesystem space. It can be
containerized and scaled out using common technologies like
`tmpnb <https://github.com/jupyter/tmpnb>`_,
`Cloud Foundry <https://github.com/cloudfoundry>`_, and
`Kubernetes <http://kubernetes.io/>`_.


