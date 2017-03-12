Feature Flags and Doctrine Entities
===================================

I was in a discussion with some of the `EasyBib developers
<http://drafts.easybib.com/>`_ this week about how to use feature flags with
Doctrine Entities, Metadata Mapping and their database.

The problem of feature flags with Doctrine is easily explained: If you add
properties for a new feature that is disabled in the Doctrine metadata, then you
need to upgrade the database before deployment, even when the feature is not
being rolled out for some days/weeks. Doctrine requires the database to look
exactly like the metadata specifies it.

You can get around this problem by using the `loadClassMetadata` event quite
easily:

.. code-block:: php

    <?php
    namespace MyProject\Listener;

    use MyProject\Config\FeatureFlagConfiguration;
    use Doctrine\ORM\Event\LoadClassMetadataEventArgs;

    class FeatureFlagMetadataListener 
    {
        private $featureFlagConfiguration;

        public function __construct(FeatureFlagConfiguration $config)
        {
            $this->featureFlagConfiguration = $config;
        }

        public function loadClassMetadata(LoadClassMetadataEventArgs $eventArgs)
        {
            $classMetadata = $eventArgs->getClassMetadata();

            if ($this->featureFlagConfiguration->isEnabled('super_feature2')) {

                if ($classMetadata->name === "MyProject\\Entity\\User") {
                    $classMetadata->mapField(array(
                        'fieldName' => 'superFeatureProperty',
                        'type' => 'string'
                    ));
                }

                if ($classMetadata->name === "MyProject\\Entity\\Something") {
                    // more mapping
                }
            }
        }
    }

You can find documentation on the ClassMetadata in the `documentation
<http://docs.doctrine-project.org/en/latest/reference/php-mapping.html>`_ or
`API
<http://www.doctrine-project.org/api/orm/2.4/class-Doctrine.ORM.Mapping.ClassMetadataInfo.html#methods>`_.

Then if the feature is enabled fore some time and accepted into the pool of
permanent features, you can remove the listener and move the mapping onto the
Entities metadata.

.. author:: default
.. categories:: PHP
.. tags:: Doctrine, ApplicationDesign
.. comments::
