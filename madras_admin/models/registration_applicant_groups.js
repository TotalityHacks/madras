'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('registration_applicant_groups', {
    'applicant_id': {
      type: DataTypes.INTEGER,
    },
    'group_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'registration_applicant_groups',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

