#!/usr/bin/env groovy

import hudson.model.*
import hudson.EnvVars


node {
    try {

        stage("blank") {
          currentBuild.result = "SUCCESS"
        }

    } catch(Exception err) {
        currentBuild.result = "FAILURE"
    } finally {

    }
}
