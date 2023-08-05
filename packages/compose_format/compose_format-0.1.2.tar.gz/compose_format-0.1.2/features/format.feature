@slow
Feature: Format
  As a DevOps
  I want to have readable, formatted docker-compose files
  so that I see errors soon

  Scenario: Compose Version 1
    Given a file named "compose.yml" with:
      """
      foo:
        image: bar
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      foo:
        image: bar
      """

  Scenario: Compose Version 2
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        foo:
          image: bar
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services:

        foo:
          image: bar
      """

  Scenario: Service Sort Order
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        d_service:
          image: image
        c_service:
          image: image
        b_service:
          image: image
        a_service:
          image: image
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services:

        a_service:
          image: image

        b_service:
          image: image

        c_service:
          image: image

        d_service:
          image: image
      """

  Scenario: Top Level Sort Order
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        service
      volumes:
        volume
      networks:
        network
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services: service
      volumes: volume
      networks: network
      """

  Scenario: Children Sort Order
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        service:
          image: image
          ports:
            - '2'
            - '1'
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services:

        service:
          image: image
          ports:
            - '1'
            - '2'
      """

  Scenario: Service Member Order
    Given a file named "compose.yml" with:
      """
      version: "2"
      services:
        foo:
          image: not_relevant
          ports: not_relevant
          expose: not_relevant
          tty: not_relevant
          extra_hosts: not_relevant
          restart: not_relevant
          command: not_relevant
          links: not_relevant
          ulimits: not_relevant
          volumes: not_relevant
          volumes_from: not_relevant
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services:

        foo:
          image: not_relevant
          command: not_relevant
          links: not_relevant
          volumes_from: not_relevant
          volumes: not_relevant
          expose: not_relevant
          ports: not_relevant
          extra_hosts: not_relevant
          restart: not_relevant
          ulimits: not_relevant
          tty: not_relevant
      """

  Scenario: Stringify Numbers
    Given a file named "compose.yml" with:
      """
      version: 2
      services:
        foo:
          ports:
            - 10000
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '2'
      services:

        foo:
          ports:
            - '10000'
      """
