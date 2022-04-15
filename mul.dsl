multibranchPipelineJob('htask')
{
 branchSources
 {
  branchSource
  {
   source
   {
    git
    {
     id('h-handler-v1')
       
       remote('https://github.com/meiyarasu/Project4.git')

       traits
       {
        submoduleOptionTrait
        {
         extension
         {
          disableSubmodules(false)
                           recursiveSubmodules(true)
                           trackingSubmodules(false)
                           reference(null)
                           timeout(null)
                           parentCredentials(true)
                           }
         }

        cloneOptionTrait {
                          extension {
                                     shallow (false)
                                             noTags (false)
                                             reference (null)
                                             depth(0)
                                             honorRefspec (false)
                                             timeout (10)
                                             }
                                    }
        }
       }
    }
   }
  }

  orphanedItemStrategy
  {
   discardOldItems
   {
    numToKeep(-1)
             }
   }

  configure
  {
   def traits = it / sources / data / 'jenkins.branch.BranchSource' / source / traits
       traits << 'jenkins.plugins.git.traits.BranchDiscoveryTrait' {
        strategyId(3)
       }
  }

  configure {
        def traits = it / sources / data / 'jenkins.branch.BranchSource' / source / traits
        traits << 'jenkins.plugins.git.traits.BranchDiscoveryTrait' {}
        traits << 'jenkins.plugins.git.traits.WipeWorkspaceTrait'() {
            extension( class: 'hudson.plugins.git.extensions.impl.WipeWorkspace' ) 
        }
    }

  configure
  {
   def traits = it / sources / data / 'jenkins.branch.BranchSource' / source / traits
       traits << 'jenkins.scm.impl.trait.WildcardSCMHeadFilterTrait' {
        includes('feature/* develop dev-* sit-* prd-* cpt-* uat-*') // detect all branches
        excludes('master')
       }
  }

  configure
  {
   def traits = it / sources / data / 'jenkins.branch.BranchSource' / source / traits
       traits << 'jenkins.plugins.git.traits.TagDiscoveryTrait' {
            strategyId(3)
       }
   }

 }
