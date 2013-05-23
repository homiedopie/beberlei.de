Symfony2 on Windows Azure Websites
==================================

With the Windows Azure Websites platform-as-a-service (PaaS), which was
released as a preview to a general audiance in June last year, PHP applications
can be deployed to Azure with as much as a Git push to a remote repository. At
the same time Microsoft released a new and much improved `PHP SDK
<https://github.com/WindowsAzure/azure-sdk-for-php>`_, which
integrates with all the Azure webservices.

I blogged about deployment with Composer on Azure Websites last November and
since then I have been working with Microsoft to improve Symfony2 support on
Windows Azure by developing and releasing the `AzureDistributionBundle
<https://github.com/beberlei/AzureDistributionBundle>`_. This is a new version
of the bundle and contains the following improvements:

- Full support for the PHP SDK through the DependencyInjection container
- Installation of project dependendencies using Composer during deployment.
  I will blog about the Composer support in much more detail in the next
  days, because this information is not only valuable for Symfony2 projects.
- a `full demo application
  <https://github.com/beberlei/symfony-azure-edition>`_ (derived from
  symfony-standard) to show PHP, Symfony & Azure integration
- documentation of the Windows Azure Websites deployment process and
  possiblities for PHP configuration
- a Stream Wrapper for Azure Blob Storage, currently being reviewed for
  inclusion into the Azure PHP SDK itself.

You can install both the Bundle or the Demo application via Composer.
For the Demo application call:

::

    $ php composer.phar create-project beberlei/symfony-azure-edition

The README includes more information about how to deploy the demo
to your Azure websites account.

The bundle can be installed using the following ``composer.json``::

    {
        "require": {
            "beberlei/azure-distribution-bundle": "*"
        },
        "repositories": [
            {
                "type": "pear",
                "url": "http://pear.php.net"
            }
        ],
    }

Registering PEAR is necessary, because the Azure PHP SDK depends on some PEAR
components.

.. author:: default
.. categories:: PHP
.. tags:: Azure
.. comments::
