.. vim:sw=3 ts=3 expandtab tw=78

VESNA ALH Authentication proxy
==============================

This package contains a deamon (``vesna_alh_auth_proxy``) that proxies
ALH requests from a Unix domain socket to an ALH web end-point. It performs
authentication based on the system user originating request. This enables
multiple users on a system to share the same credentials for the ALH web
end-point, without exposing the credentials to them.

An ALH implementation class ``vesna.omf.ALH`` is also provided that uses the
service provided by the proxy. Compared to the usual ``ALHWeb`` class, this
does not require any parameters for its construction. ``base_url`` and
``cluster_id`` are added by the proxy from its configuration file based on
``cluster_uid``. ``cluster_uid`` is set from the environment, which typically
comes from the OMF Resource Proxy.
