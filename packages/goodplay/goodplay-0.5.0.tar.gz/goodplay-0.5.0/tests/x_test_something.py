from goodplay_helpers import smart_create


def test_something(testdir):
    smart_create(testdir.tmpdir, '''
    ## .goodplay.yml
    platforms:
      - name: EL
        version: 6
        image: busybox:latest

    ## meta/main.yml
    galaxy_info:
      author: Benjamin Schwarze
      platforms:
        - name: EL
          versions:
            - 6
    dependencies: []

    ## tasks/main.yml
    - ping:

    ## tests/inventory
    host1 goodplay_platform=*
    #host1 goodplay_image=*

    ## tests/test_playbook.yml
    - hosts: host1
      gather_facts: no
      tasks:
        - name: host is reachable
          ping:
          tags: test
    ''')

    result = testdir.inline_run('-s')
    result.assertoutcome(passed=1)
